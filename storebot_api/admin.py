from django.contrib import admin
from .models import Brand, Product

admin.site.register(Product)
admin.site.register(Brand)