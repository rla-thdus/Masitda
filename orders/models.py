from django.db import models

from restaurants.models import Menu
from users.models import User


class Blanket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
