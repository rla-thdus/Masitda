from django.core.management import BaseCommand
from restaurants.models import FoodCategory


class Command(BaseCommand):
    help = 'init setting food category'

    def handle(self, *args, **options):
        categories = [
            '족발,보쌈',
            '찜,탕,찌개',
            '돈까스,회,일식',
            '피자',
            '고기,구이',
            '야식',
            '양식',
            '치킨',
            '중식',
            '아시안',
            '백반,죽,국수',
            '도시락',
            '분식',
            '카페,디저트',
            '패스트푸드'
        ]
        for c in categories:
            FoodCategory.objects.create(type=c)
        self.stdout.write(self.style.SUCCESS("Initial food category created"))
