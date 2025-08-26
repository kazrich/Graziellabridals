from django.urls import path
from . import views

urlpatterns = [
    # -------------------------------
    # 🔐 Auth & Registration
    # -------------------------------
    path('register/', views.register_client, name='register_client'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # -------------------------------
    # 🔁 Password Recovery
    # -------------------------------
    path('recover-password/', views.recover_password, name='recover_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    

    # -------------------------------
    # 💖 Wishlist
    # -------------------------------
    path('get-wishlist/', views.get_wishlist, name='get_wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('view-wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist-drawer/', views.wishlist_drawer, name='wishlist_drawer'),
]
