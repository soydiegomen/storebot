from django.shortcuts import render
from django.db.models import *
from django.db import transaction
""" from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication """
""" from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView


from rest_framework import status """
from rest_framework import permissions
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
""" from rest_framework import viewsets """
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
from core.serializers import *
from core.models import *


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