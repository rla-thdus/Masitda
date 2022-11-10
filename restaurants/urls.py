from django.urls import path

from . import views

app_name = "restaurants"

urlpatterns = [
    path('', views.RestaurantAPI.as_view(), name='restaurants')
]