from django.contrib import admin

from orders.models import Cart, BlanketItem


@admin.register(Cart)
class BlanketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']


@admin.register(BlanketItem)
class BlanketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'blanket', 'menu', 'quantity']
