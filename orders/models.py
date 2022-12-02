from django.db import models

from restaurants.models import Menu
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BlanketItem(models.Model):
    blanket = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='blanket_items')
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
