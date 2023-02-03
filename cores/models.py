from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

from accounts.models import User
from api import settings


class FoodCategory(models.Model):
    type = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.id} {self.type}'


class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cores')
    name = models.CharField(max_length=256, unique=True)
    category = models.ManyToManyField(FoodCategory, blank=True)
    address = models.TextField()
    phone = PhoneNumberField(unique=True, null=True)
    content = models.TextField()
    min_order_price = models.PositiveIntegerField()
    delivery_price = models.PositiveIntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    @property
    def rating_avg(self):
        reviews = Review.objects.filter(order__cart__restaurant_id=self.id)
        return f"{sum([item.rating for item in reviews]) / len(reviews):.1f}"


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.id} {self.name}'


def bigger_or_equal_than_1(value):
    if value < 1:
        raise ValidationError("Ensure this value is greater than or equal to 1.")


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_at = models.DateTimeField(blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def total_price(self):
        return sum([item.price for item in self.cart_items.all()])


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
        return self.cart.total_price

    @property
    def delivery_price(self):
        return self.cart.restaurant.delivery_price

    @property
    def amount_payment(self):
        return self.cart.total_price + self.delivery_price

    @property
    def restaurant(self):
        return self.cart.restaurant

class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)
    rating = models.FloatField(default=1, validators=[MaxValueValidator(5.0), MinValueValidator(0.5)])
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user(self):
        return self.order.cart.user

    @property
    def restaurant(self):
        return self.order.restaurant

