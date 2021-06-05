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

        if 'brand_id' not in request.data:
            return Response({'message' : 'The brand_id field is required'}, 400)

        brand_id = request.data['brand_id']
        brand = get_object_or_404(Brand,id = brand_id)

        serializer = ProductSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        #The new products are always active
        serializer.save(brand = brand, is_active = True) 
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):

        product_id = self.kwargs.get("product_id")
        producto = get_object_or_404(Product,id = product_id)

        brand_id = request.data['brand_id']
        brand = get_object_or_404(Brand,id = brand_id)

        is_active = producto.is_active
        if 'is_active' in request.data:
            is_active = request.data['is_active']

        # .save() will update the existing `comment` instance.
        product_serializer = ProductSerializer(producto, data = request.data)

        if not product_serializer.is_valid():
            return Response(product_serializer.errors)

        product_serializer.save(brand = brand, is_active = is_active)
        
        return Response(product_serializer.data)