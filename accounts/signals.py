from django.utils import timezone
from django.utils.timezone import localtime
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import UserLogin, UserRegistration

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if isinstance(user, UserRegistration):
        local_timestamp = localtime(timezone.now())
        UserLogin.objects.create(user=user, timestamp=local_timestamp, success=True)
