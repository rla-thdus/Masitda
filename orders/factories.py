import factory

from orders.models import Cart, CartItem


class BlanketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = ''


class BlanketItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    blanket = ''
    menu = ''
    quantity = factory.Faker('pyint')
