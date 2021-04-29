from rest_framework import serializers
from rest_framework.authtoken.models import Token
from storebot_api.models import *


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"