import datetime

import factory

from cores.models import Restaurant, FoodCategory, Menu, Cart, CartItem, OrderStatus, Order, Review
from accounts.factories import fake


class FoodCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodCategory

    type = factory.Faker('name')


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant

    user = ''
    name = factory.Faker('name')
    address = factory.Faker('address')
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    content = factory.Faker('sentence')
    min_order_price = factory.Faker('pyint')
    delivery_price = factory.Faker('pyint')
    open_time = factory.Faker('time')
    close_time = factory.Faker('time')


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu

    restaurant = ''
    name = factory.Faker('name')
    price = factory.Faker('pyint')
    description = factory.Faker('sentence')


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = ''


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = ''
    menu = ''
    quantity = factory.Faker('pyint')


class OrderStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderStatus

    name = factory.Faker('name')

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    cart = ''
    order_status = ''


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    order = ''
