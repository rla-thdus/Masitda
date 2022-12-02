from django.contrib import admin

from orders.models import Cart, CartItem


@admin.register(Cart)
class BlanketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']


@admin.register(CartItem)
class BlanketItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'menu', 'quantity']
