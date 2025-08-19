from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from .views import ask_popup

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
    path('ask-popup/', ask_popup, name='ask_popup'),
        # ... your other paths
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about-us/', views.about_us, name='about-us'),
 
]
