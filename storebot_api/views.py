from django.shortcuts import render
from django.db.models import *
from django.db import transaction
from storebot_api.serializers import *
from storebot_api.models import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.html import strip_tags
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from datetime import datetime
from django.conf import settings
from django.template.loader import render_to_string


from .models import Brand
#from . import serializers

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        roles = user.groups.all()
        role_names = []
        for role in roles:
            role_names.append(role.name)
        
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'token': token.key,
                'roles': role_names
            })
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class UsuarioActualView(generics.RetrieveAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        user = request.user

        data = UserSerializer(user).data

        return Response(data)


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



class AdminsView(generics.ListCreateAPIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        
        secret = self.kwargs.get('secret')

        if secret != settings.ADMIN_SECRET:
            return Response({},403)
        
        username = request.data['username']
        user = User.objects.filter(username=username).first()
        if user:
            return Response({"mensaje":"The username '"+username+"' exist"},400)

        user = User.objects.create(username=username,
                            first_name=request.data['first_name'],
                            last_name=request.data['last_name'],
                            email=request.data['email'])

        user.set_password(request.data['password'])

        group, created = Group.objects.get_or_create(name='admin')
        group.user_set.add(user)
        user.save()

        return Response({"id":user.id}, 201)

class Brands(APIView):

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