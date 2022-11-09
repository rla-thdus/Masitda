from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path('', views.RestaurantAPI.as_view(), name='restaurant')
]