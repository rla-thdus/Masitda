import factory

from orders.models import Cart, CartItem, OrderStatus


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
