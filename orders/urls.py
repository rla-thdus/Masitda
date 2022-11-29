from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path('<int:user_id>', views.BlanketAPI.as_view()),
]