from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    name = models.CharField(max_length=255,null=False, blank=False)
    description = models.CharField(max_length=255,null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    image = models.ImageField(upload_to='image/%Y-%m-%d/', null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.name