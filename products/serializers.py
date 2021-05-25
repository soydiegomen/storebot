from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"