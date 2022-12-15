import random

from django.contrib.admin.utils import flatten
from django.core.management import BaseCommand
from django_seed import Seed

from cores.models import Restaurant, FoodCategory
from accounts.models import User


class Command(BaseCommand):
    help = 'create cores'

    def add_arguments(self, parser):
        parser.add_argument('--number', default=1, type=int)

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {
            'role': '사장',
            'is_admin': False,
            'is_staff': False
        })
        created = seeder.execute()
        user= User.objects.get(id=flatten(list(created.values()))[0])

        seeder.add_entity(Restaurant, number, {
            'user': user,
        })
        created_restaurant = seeder.execute()
        created_restaurant_pk_list = flatten(list(created_restaurant.values()))
        category = FoodCategory.objects.first()
        for c in created_restaurant_pk_list:
            restaurant = Restaurant.objects.get(pk=c)
            restaurant.category.add(category)
        self.stdout.write(self.style.SUCCESS(f"{number}개의 음식점이 작성 되었습니다."))
