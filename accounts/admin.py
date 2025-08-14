from django.contrib import admin
from .models import (
    UserRegistration,
    UserLogin,
    PasswordRecovery,
    ClientProfile,
    WishlistItem
)

# -------------------------------
# 👤 User Registration
# -------------------------------

@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name',)


# -------------------------------
# 🔓 User Login Tracking
# -------------------------------

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('styled_user', 'timestamp', 'success_icon')
    list_filter = ('success', 'timestamp')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    ordering = ('-timestamp',)
    list_per_page = 20

    def styled_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".title()
    styled_user.short_description = "Client Name"

    def success_icon(self, obj):
        return "✅" if obj.success else "❌"
    success_icon.short_description = "Login Status"


# -------------------------------
# 🔁 Password Recovery
# -------------------------------

@admin.register(PasswordRecovery)
class PasswordRecoveryAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__email', 'token')
    ordering = ('-created_at',)


# -------------------------------
# 💼 Client Profile (Optional)
# -------------------------------

# If you're not using ClientProfile actively, you can skip registering it.
# If you plan to use it later, uncomment below:

# @admin.register(ClientProfile)
# class ClientProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number', 'created_at')
#    search_fields = ('user__email', 'phone_number')


# -------------------------------
# 💖 Wishlist Items
# -------------------------------

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'product_name',
        'product_id',
        'notes',
        'added_at'
    ]
    list_editable = ['notes']
    search_fields = (
        "product_name",
        "product_id",
        "notes",
        "user_login__user__email"
    )
    list_filter = ("added_at",)
    ordering = ("-added_at",)
    list_per_page = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user_login", "user_login__user")

    def user_email(self, obj):
        return obj.user_login.user.email
    user_email.short_description = "Client Email"
