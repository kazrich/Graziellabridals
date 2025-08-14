from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# -------------------------------
# 👤 Client Profile
# -------------------------------

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Client Profile"
        verbose_name_plural = "Client Profiles"
        ordering = ['last_name', 'first_name']


# -------------------------------
# 🔐 User Registration
# -------------------------------

class UserRegistration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    class Meta:
        verbose_name = "User Registration"
        verbose_name_plural = "User Registrations"
        ordering = ['last_name', 'first_name']


# -------------------------------
# 🔓 User Login Tracking
# -------------------------------

class UserLogin(models.Model):
    user = models.ForeignKey(UserRegistration, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        status = "Success" if self.success else "Failed"
        user_email = self.user.email if self.user else "Unknown"
        return f"{user_email} at {self.timestamp.strftime('%Y-%m-%d %H:%M')} — {status}"

    class Meta:
        verbose_name = "User Login"
        verbose_name_plural = "User Logins"
        ordering = ['-timestamp']


# -------------------------------
# 🔁 Password Recovery
# -------------------------------

class PasswordRecovery(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recovery for {self.user.email}"

    class Meta:
        verbose_name = "Password Recovery"
        verbose_name_plural = "Password Recoveries"
        ordering = ['-created_at']


# -------------------------------
# 💖 Wishlist Item
# -------------------------------

class WishlistItem(models.Model):
    user_login = models.ForeignKey(UserLogin, on_delete=models.CASCADE, null=True)
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=255)
    product_image = models.URLField()
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        user_name = self.user_login.user.first_name if self.user_login and self.user_login.user else "Unknown"
        return f"{user_name}'s wishlist: {self.product_name}"

    class Meta:
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        ordering = ['-added_at']


# -------------------------------
# 🚪 Logout Event
# -------------------------------

class LogoutEvent(models.Model):
    user_login = models.ForeignKey(UserLogin, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_email = self.user_login.user.email if self.user_login and self.user_login.user else "Unknown"
        return f"Logout by {user_email} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Logout Event"
        verbose_name_plural = "Logout Events"
        ordering = ['-timestamp']
