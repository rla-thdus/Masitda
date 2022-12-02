import factory

from orders.models import Cart, BlanketItem


class BlanketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = ''


class BlanketItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlanketItem

    blanket = ''
    menu = ''
    quantity = factory.Faker('pyint')
