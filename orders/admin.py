from django.contrib import admin

from orders.models import Blanket


@admin.register(Blanket)
class BlanketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
