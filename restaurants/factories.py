import factory

from restaurants.models import Restaurant, FoodCategory, Menu


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


class FoodCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodCategory
