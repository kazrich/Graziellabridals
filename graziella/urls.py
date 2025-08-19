from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
        # ... your other paths
    path('logout/', LogoutView.as_view(), name='logout'),
    path('about-us/', views.about_us, name='about-us'),
 
]
