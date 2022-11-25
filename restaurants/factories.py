import factory

from restaurants.models import Restaurant, FoodCategory, Menu


class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant


class MenuFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Menu


class FoodCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodCategory
