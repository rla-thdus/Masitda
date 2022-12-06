import factory

from orders.models import Cart, CartItem


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
