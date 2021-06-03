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
from .models import Product
from storebot_api.models import Brand
from .serializers import ProductSerializer


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

        brand_id = request.data['brand_id']
        brand = get_object_or_404(Brand,id = brand_id)

        data = request.data
        serializer = ProductSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        serializer.save(user=user, brand = brand, is_active = True) 
        response = serializer.data
        
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