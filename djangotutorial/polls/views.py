from urllib import request
from django.http import JsonResponse


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


from .models import Product, Category, Shop, Order, ProductInfo
from .serializers import ProductSerializer, CategorySerializer, ShopSerializer, OrderSerializer, ProductInfoSerializer


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
        product = ProductInfo.objects.get(id=id).prefetch_related('information__product_info__product__category').annotate()
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
    #     serializer = CategorySerializer(categories, many=True)
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


