# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
import secrets

from .models import UserRegistration

token = secrets.token_urlsafe(32)

from django.urls import reverse
from django.urls import reverse_lazy



from .forms import RegistrationForm, LoginForm, PasswordRecoveryForm
from .models import UserRegistration, PasswordRecovery
from django.contrib.auth.hashers import check_password
from .models import UserRegistration, UserLogin  # Adjust if needed
from django.utils import timezone

# -------------------------------
# 🔐 Registration View
# -------------------------------


def register_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # Validate fields
        if not all([first_name, last_name, email, password]):
            messages.error(request, "All fields are required.")
            return redirect('register_client')

        # Check for existing email
        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_client')

        # Hash password
        hashed_password = make_password(password)

        # Save to database
        UserRegistration.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')  # Or wherever you want to send them

    return render(request, 'form.html')
# -------------------------------
# 🔓 Login View
# -------------------------------


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'form.html', {'form': LoginForm()})

        try:
            registration = UserRegistration.objects.get(email=email)
            login_success = check_password(password, registration.password)

            # ✅ Log the login attempt
            UserLogin.objects.create(
                user=registration,
                timestamp=timezone.now(),
                success=login_success
            )

            if login_success:
                # ✅ Store session data for personalization
                request.session['user_id'] = registration.id
                request.session['user_name'] = registration.first_name
                request.session.set_expiry(1209600 if remember_me else 0)

                messages.success(
                    request,
                    f"Hello, Welcome to Graziella Bridals, {registration.first_name}!"
                )
                return redirect('home')
            else:
                messages.error(request, "Incorrect password. Please try again.")

        except UserRegistration.DoesNotExist:
            # ❌ Log failed attempt with no user
            UserLogin.objects.create(
                user=None,
                timestamp=timezone.now(),
                success=False
            )
            messages.error(request, "No account found with that email.")

    # 🧘 Graceful fallback to login form
    return render(request, 'form.html', {'form': LoginForm()})


# -------------------------------
# 📩 Recover Password View
# -------------------------------

def recover_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            registration = UserRegistration.objects.get(email=email)

            token = secrets.token_urlsafe(32)
            PasswordRecovery.objects.create(user=registration, token=token)

            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={'token': token})
            )

            send_mail(
                subject="Graziella Bridals Password Reset",
                message=f"Click the link to reset your password:\n{reset_link}",
                from_email="no-reply@graziella.com",
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(request, "Recovery email sent! Please check your inbox.")
            return redirect('login')
        except UserRegistration.DoesNotExist:
            messages.error(request, "No account found with that email.")

    return render(request, 'accounts/recover_form.html')

# -------------------------------
# 🔁 Reset Password View
# -------------------------------

# -------------------------------
# 🔁 Reset Password View
# -------------------------------

def reset_password(request, token):
    try:
        recovery_entry = PasswordRecovery.objects.get(token=token)
    except PasswordRecovery.DoesNotExist:
        messages.error(request, "Invalid or expired reset link.")
        return redirect('login')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        if not new_password:
            messages.error(request, "Please enter a new password.")
            return render(request, 'accounts/recover_form.html', {'token': token})

        # ✅ Update password inside UserRegistration
        registration = recovery_entry.user
        registration.password = make_password(new_password)
        registration.save()

        recovery_entry.delete()

        messages.success(request, "Your password has been reset successfully.")
        return redirect('login')

    return render(request, 'accounts/recover_form.html', {'token': token})

