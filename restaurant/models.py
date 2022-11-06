from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class FoodCategory(models.Model):
    type = models.CharField(max_length=256)


class Restaurant(models.Model):
    name = models.CharField(max_length=256)
    category = models.ManyToManyField(FoodCategory)
    address = models.TextField()
    phone = PhoneNumberField(unique=True, null=True)
    content = models.TextField()
    min_order_price = models.IntegerField()
    delivery_price = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()
