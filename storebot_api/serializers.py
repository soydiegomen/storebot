from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Brand, BrandUrl


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"

class BrandUrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandUrl
        fields = "__all__"