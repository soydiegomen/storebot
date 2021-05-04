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
from .models import Brand, Product
from .serializers import ProductSerializer, BrandSerializer


class ProductsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    
    def get(self, request, *args, **kwargs):

        filter = Q(isActive=True)

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

        if 'isActive' in request.data:
            producto.isActive = request.data['isActive']

        producto.save()

        response = ProductSerializer(producto, many=False).data

        return Response(response)

class BrandsViews(APIView):

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
    
    def get(self, request):
        restaurants = Brand.objects.all()
        serializer = BrandSerializer(restaurants, many=True)
        return Response(serializer.data)