from django.contrib import admin

from orders.models import Blanket


@admin.register(Blanket)
class BlanketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'menu_id', 'count']

    def menu_id(self, obj):
        return obj.menu.id
