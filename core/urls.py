from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('token/', views.CustomAuthToken.as_view()),
    #User details
    path('me', views.UsuarioActualView.as_view()),
    #Create admin
    path('usuarios/admin/<str:secret>', views.AdminsView.as_view()),
]