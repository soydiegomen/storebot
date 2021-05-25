from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from .views import ProductsView

urlpatterns = [
    #Productos
    path('products',  ProductsView.as_view()),
    path('products/<int:id_producto>', ProductsView.as_view()),
]