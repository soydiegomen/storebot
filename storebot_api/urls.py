
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from .views import BrandsViews, BrandUrlsViews

urlpatterns = [
    #Agrego las urls del core
    path(r'', include('core.urls')),        
    #Productos
    path(r'', include('products.urls')),        
    #Brands
    path('brands', BrandsViews.as_view()),
    path('brands/<int:brand_id>', BrandsViews.as_view()),
    path('brandUrls', BrandUrlsViews.as_view()),
    path('brandUrls/<int:brandUrl_id>', BrandUrlsViews.as_view()),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

