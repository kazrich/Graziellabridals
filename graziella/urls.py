from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import register_view

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
    path('form/', views.form, name='form'), 
]
