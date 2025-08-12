# accounts/urls.py
from django.urls import path
from . import views
from .views import register_client, login_view

urlpatterns = [
    path('register/', views.register_client, name='register_client'),
    path('login/', login_view, name='login'),
    path('recover-password/', views.recover_password, name='recover_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
]

