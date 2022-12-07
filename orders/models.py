from django.db import models
from rest_framework.exceptions import ValidationError

from restaurants.models import Menu
from users.models import User


def bigger_or_equal_than_1(value):
    if value < 1:
        raise ValidationError("Ensure this value is greater than or equal to 1.")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[bigger_or_equal_than_1])
