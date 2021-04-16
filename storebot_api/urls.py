"""storebot_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from storebot_api.views import auth
from storebot_api.views import usuarios
from storebot_api.views import products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', auth.CustomAuthToken.as_view()),
    #User details
    path('me',usuarios.UsuarioActualView.as_view()),
    #Create admin
    path('usuarios/admin/<str:secret>',usuarios.AdminsView.as_view()),
    #Productos
    path('products',products.ProductsView.as_view()),
    path('product/<int:id_producto>',products.ProductsView.as_view()),

] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

