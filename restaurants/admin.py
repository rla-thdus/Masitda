from django.contrib import admin
from restaurants.models import Restaurant, FoodCategory

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'phone', 'get_category', 'phone', 'content', 'min_order_price', 'delivery_price', 'open_time', 'close_time']

    def get_category(self, obj):
        return obj.category.all()


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']