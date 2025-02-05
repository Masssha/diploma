from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
# , RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class PAPIView(APIView):
    def get(self, request):
        data = {'m': 'e'}
        return Response(data)


class ProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_product_by_id(self, request):
        id = request.data.get('id')
        data = Product.objects.all.get(id=id)
        ser = ProductSerializer(data)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        ser = ProductSerializer(data=request.data)
        ser.save()
        return Response(ser.data)






# from django.http import HttpResponse
#
#
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
