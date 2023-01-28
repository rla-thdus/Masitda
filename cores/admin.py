from django.contrib import admin
from cores.models import Restaurant, FoodCategory, Menu, Cart, CartItem, OrderStatus, Order, Review


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone', 'get_category', 'phone', 'content', 'min_order_price', 'delivery_price', 'open_time', 'close_time']

    def get_category(self, obj):
        return obj.category.all()


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant_id', 'name', 'price', 'description']

    def restaurant_id(self, obj):
        return obj.restaurant.id


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant_id', 'created_at', 'ordered_at']

    def restaurant_id(self, obj):
        if obj.restaurant is not None:
            return obj.restaurant.id
        return ''


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'menu', 'quantity', 'price']


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'user_id', 'restaurant_id', 'total_price', 'delivery_price', 'amount_payment', 'order_status', 'date']

    def user_id(self, obj):
        return obj.cart.user.id

    def restaurant_id(self, obj):
        return obj.restaurant.id

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'text', 'created_at']
