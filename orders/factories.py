import factory

from orders.models import Blanket, BlanketItem


class BlanketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blanket

    user = ''


class BlanketItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlanketItem

    blanket = ''
    menu = ''
    quantity = factory.Faker('pyint')
