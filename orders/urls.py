from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path('items/<int:item_id>', views.CartItemAPI.as_view()),
    path('', views.CartAPI.as_view()),
]