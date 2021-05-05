from django.contrib import admin
from .models import Brand, Product, BrandUrl

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(BrandUrl)