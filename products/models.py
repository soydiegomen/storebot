from django.db import models
#from django_enumfield import enum
#from django.db.models.signals import post_save
from django.contrib.auth.models import User
from storebot_api.models import Brand

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False, blank=False, default=None)
    url = models.CharField(max_length=512, null=False, blank=False)
    price = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    discount = models.DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    final_price = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    sku = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True, default=0)
    views = models.IntegerField(null=False, blank=True, default=0)
    instagram_likes = models.IntegerField(null=False, blank=True, default=0)
    is_active = models.BooleanField(null=False, blank=False, default=True)
    GENDER_CHOICES = [
        ('MAN', 'MAN'),
        ('WOMAN', 'WOMAN'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )
    #image = models.ImageField(upload_to='image/%Y-%m-%d/', null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name