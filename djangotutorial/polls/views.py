from urllib import request

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
import aiohttp
from rest_framework.authtoken.models import Token
from django.db.models import Sum, F, Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
# , RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


from .models import Product, Category, Shop, Order, ProductInfo, Contact, ConfirmEmailToken
from .serializers import ProductSerializer, CategorySerializer, ShopSerializer, OrderSerializer, ProductInfoSerializer, \
    ContactSerializer, PersonSerializer


class ProductsAPIView(ListAPIView):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

    def get(self, request):
        shop_id = request.query_params.get('shop_id')
        queryset = ProductInfo.objects.all()

        if shop_id:
            query = Q(shop_id=shop_id)
            queryset = ProductInfo.objects.filter(query)

        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(ListAPIView):
    serializer_class = ProductInfoSerializer

    def get_object(self, id):
        try:
            return ProductInfo.objects.get(id=id)
        except ProductInfo.DoesNotExist:
            raise Http404

    def get(self, request, id):
        product = ProductInfo.objects.prefetch_related('product__category').get(id=id)
        # product = ProductInfo.objects.get(id=id).prefetch_related('information__product_info__product__category').annotate()
        serializer = ProductInfoSerializer(product)
        return Response(serializer.data)


    def put(self, request, id):
        product = self.get_object(id)
        serializer = ProductInfoSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoriesView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

#неудачные попытки сделать асинхронные функции:
# class CategoriesView(ListAPIView):
#     serializer_class = CategorySerializer
#     async def get(self, request):
#         async with aiohttp.ClientSession() as session:
#             async with session.get('http://127.0.0.1:8000/polls/categories/') as response:
#                 categories = await Category.objects.all()  # Получаем все категории асинхронно.
#                 serializer = await CategorySerializer(categories, many=True)
#                 return Response(serializer.data, status=status.HTTP_200_OK)




    # async def connect(self):
    #     self.username = await get()
    #



    # @database_sync_to_async
    # def get(self, request, *args, **kwargs):
    #     categories = Category.objects.all()
    #     serializer = CategorySerializer(categories, many=True)
    #     return Response(serializer.data)




    # async def get(self, request, *args, **kwargs):
    #     categories = await sync_to_async(Category.objects.all())()  # Получаем все категории асинхронно.
    #     serializer = await sync_to_async(CategorySerializer(categories, many=True))
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class ShopsView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class BasketView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(user_id=request.user.id, state='basket').prefetch_related('ordered_items__product_info__product__category', 'ordered_items__product_info__product_parameter__parameter').annotate(total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    # def post(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)


class PartnerOrders(APIView):
    """
        Класс для получения заказов поставщиками
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'owner':
            return JsonResponse({'Status': False, 'Error': 'For owner only'}, status=403)

        order = Order.objects.filter(
            ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class ContactView(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'city', 'street', 'phone'}.issubset(request.data):
            request.data._mutable = True
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Indicate your complete address'})



class OrderView(APIView):
    """
    Класс для получения и размешения заказов пользователями
    """

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        order = Order.objects.filter(user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()

        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class RegisterAccount(APIView):
    def post(self, request, *args, **kwargs):
        if {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                user_serializer = PersonSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

class ConfirmAccount(APIView):
    def post(self, request, *args, **kwargs):
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountDetails(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        serializer = PersonSerializer(request.user)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if 'password' in request.data:
            errors = {}
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])

        user_serializer = PersonSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

class LoginAccount(APIView):
    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])

            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)

                    return JsonResponse({'Status': True, 'Token': token.key})

            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
