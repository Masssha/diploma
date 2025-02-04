from django.db.models import Sum, F
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
# , RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

from .models import Product, Category, Shop, Order
from .serializers import ProductSerializer, CategorySerializer, ShopSerializer, OrderSerializer


class ProductsAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





        # id = request.data.get('id')
    #     data = Product.objects.all.get(id=id)
    #     ser = ProductSerializer(data)
    #     return Response(ser.data)
    #
    # def post(self, request, *args, **kwargs):
    #     ser = ProductSerializer(data=request.data)
    #     ser.save()
    #     return Response(ser.data)

class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopsView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class BasketView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):

        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(user_id=request.user.id, state='basket')
        #.prefetch_related(
        # 'orderitem__product_info__product__category',
        # 'orderitem__product_info__product_parameters__parameter').annotate(
        # total_sum=Sum(F('orderitem__quantity') * F('orderitem__product_info__price'))).distinct())
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)






# from django.http import HttpResponse
#
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
