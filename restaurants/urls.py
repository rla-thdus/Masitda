from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path('', views.RestaurantAPI.as_view(), name='restaurants'),
    path('<int:restaurant_pk>', views.RestaurantDetailAPI.as_view()),
    path('<int:restaurant_pk>/menus', views.MenuAPI.as_view(), name='menus'),
    path('<int:restaurant_pk>/menus/<int:menu_pk>', views.MenuDetailAPI.as_view())
]