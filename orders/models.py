from django.db import models

from restaurants.models import Menu
from users.models import User


class Blanket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blankets')
    menus = models.OneToOneField(Menu, on_delete=models.CASCADE, related_name='blankets')
    count = models.IntegerField(default=1)
