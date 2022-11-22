from django.core.management import BaseCommand
from django_seed import Seed

from users.models import User


class Command(BaseCommand):
    help = 'create owners'

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
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number}명의 사장이 작성 되었습니다."))
