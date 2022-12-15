from django.urls import path

from . import views

app_name = "cores"

urlpatterns = [
    path('', views.RestaurantAPI.as_view(), name='cores'),
    path('<int:restaurant_pk>', views.RestaurantDetailAPI.as_view()),
    path('<int:restaurant_pk>/menus', views.MenuAPI.as_view(), name='menus'),
    path('<int:restaurant_pk>/menus/<int:menu_pk>', views.MenuDetailAPI.as_view()),
    path('carts/items/<int:item_id>', views.CartItemAPI.as_view()),
    path('carts/<int:cart_id>/orders', views.OrderAPI.as_view()),
    path('carts/', views.CartAPI.as_view()),
]