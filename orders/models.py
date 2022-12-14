from django.db import models
from rest_framework.exceptions import ValidationError

from restaurants.models import Menu
from accounts.models import User


def bigger_or_equal_than_1(value):
    if value < 1:
        raise ValidationError("Ensure this value is greater than or equal to 1.")


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(blank=True, null=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[bigger_or_equal_than_1])

    @property
    def price(self):
        return self.quantity * self.menu.price


class OrderStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, default=1)

    @property
    def total_price(self):
        return sum([item.price for item in self.cart.cart_items.all()])

