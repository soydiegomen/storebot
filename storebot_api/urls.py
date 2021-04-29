from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #Agrego las urls del core
    path(r'', include('core.urls')),        
    #Productos
    path('products',  views.ProductsView.as_view()),
    path('product/<int:id_producto>', views.ProductsView.as_view()),
    #Brands
    path('brands', views.Brands.as_view()),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

