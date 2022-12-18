from django.core.management import BaseCommand

from cores.models import OrderStatus


class Command(BaseCommand):
    help = 'init setting order status'

    def handle(self, *args, **options):
        order_status = [
            '주문 접수중',
            '주문 수락',
            '주문 거절',
            '주문 취소'
        ]
        for o in order_status:
            OrderStatus.objects.create(name=o)
        self.stdout.write(self.style.SUCCESS("Initial order status created"))
