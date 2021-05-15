from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
from core.serializers import *
from .models import Brand, Product, BrandUrl
from .serializers import ProductSerializer, BrandSerializer, BrandUrlSerializer


class ProductsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):

        filter = Q(is_active=True)

        description = request.GET.get('description')
        if description:
            filter = filter & (Q(description__icontains=description) | Q(name__icontains=description))

        products = Product.objects.filter(filter).order_by('id').all()
        return Response(ProductSerializer(products, many=True).data)

    def post(self, request, *args, **kwargs):
        user = request.user

        name = request.data['name']
        description = request.data['description']
        quantity = request.data['quantity']
        price = request.data['price']

        product = Product.objects.create(name = name, user=user, 
        description=description, quantity=quantity, price= price)

        image = request.data['image']
        if image:
            product.image.save(image.name, image, save=True)

        response = ProductSerializer(product, many=False).data
        
        return Response(response)

    def put(self, request, *args, **kwargs):

        id_producto = self.kwargs.get("id_producto")
        producto = get_object_or_404(Product,id = id_producto)

        producto.name = request.data['name']
        producto.description = request.data['description']
        producto.quantity = request.data['quantity']
        producto.price = request.data['price']

        if 'is_active' in request.data:
            producto.is_active = request.data['is_active']

        producto.save()

        response = ProductSerializer(producto, many=False).data

        return Response(response)

class BrandsViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        restaurants = Brand.objects.filter(is_active=True).all()
        serializer = BrandSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):

        user = request.user

        name = request.data['name']
        order = request.data['order']
        url = request.data['url']
        description = request.data['description']
        rating = request.data['rating']
        order = request.data['order']

        brand = Brand.objects.create(name = name, user=user, url=url, rating=rating,
        description=description, order=order)

        response = BrandSerializer(brand, many=False).data
        
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):

        brand_id = self.kwargs.get("brand_id")
        brand = get_object_or_404(Brand, id = brand_id)

        brand.name = request.data['name']
        brand.description = request.data['description']
        brand.url = request.data['url']

        if 'is_active' in request.data:
            brand.is_active = request.data['is_active']

        if 'rating' in request.data:
            brand.rating = request.data['rating']
        else:
            brand.rating = None
        
        if 'order' in request.data:
            brand.order = request.data['order']
        else:
            brand.order = None

        brand.save()

        response = BrandSerializer(brand, many=False).data

        return Response(response)

class BrandUrlsViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        brand_urls = BrandUrl.objects.filter(is_active=True).all()
        response = BrandUrlSerializer(brand_urls, many=True)
        return Response(response.data)
    
    def post(self, request):

        id_brand = request.data['id_brand']
        brand = get_object_or_404(Brand,id = id_brand, is_active = True)

        url = request.data['url']

        brandUrl = BrandUrl.objects.create(url = url, brand = brand)

        response = BrandUrlSerializer(brandUrl, many=False).data
        
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):

        brandUrl_id = self.kwargs.get("brandUrl_id")
        brandUrl = get_object_or_404(BrandUrl, id = brandUrl_id)

        brand_id = request.data['brand_id']
        brand = get_object_or_404(Brand,id = brand_id, is_active = True)
        brandUrl.brand = brand

        if 'url' not in request.data:
            return Response({'message':'The url field is mandatory'}, 400)

        url = request.data['url']
        brandUrl.url = url

        if 'is_active' in request.data:
            brandUrl.is_active = request.data['is_active']

        brandUrl.save()

        response = BrandUrlSerializer(brandUrl, many=False).data

        return Response(response)