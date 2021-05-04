
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from .views import ProductsView, BrandsViews

urlpatterns = [
    #Agrego las urls del core
    path(r'', include('core.urls')),        
    #Productos
    path('products',  ProductsView.as_view()),
    path('product/<int:id_producto>', ProductsView.as_view()),
    #Brands
    path('brands', BrandsViews.as_view()),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

