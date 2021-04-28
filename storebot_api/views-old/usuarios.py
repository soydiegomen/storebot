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
import json
import logging

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