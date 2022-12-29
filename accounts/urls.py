from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('users', views.RegisterAPI.as_view(), name='register'),
    path('login', views.LoginAPI.as_view(), name='login'),
    path('logout', views.LogoutAPI.as_view(), name='logout')
]