from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Brand, Product, BrandUrl


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"

class BrandUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandUrl
        fields = "__all__"