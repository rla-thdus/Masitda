from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class FoodCategory(models.Model):
    type = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.id} {self.type}'


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=256, unique=True)
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
    deleted_at = models.DateTimeField(null=True)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    description = models.TextField()
