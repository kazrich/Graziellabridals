# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction

import secrets
import json

from .forms import RegistrationForm, LoginForm, PasswordRecoveryForm
from .models import (
    UserRegistration,
    UserLogin,
    PasswordRecovery,
    WishlistItem,
    LogoutEvent
)

# -------------------------------
# 🔐 Registration View
# -------------------------------

def register_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not all([first_name, last_name, email, password]):
            messages.error(request, "All fields are required.")
            return redirect('register_client')

        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_client')

        hashed_password = make_password(password)

        UserRegistration.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )

        messages.success(request, "Account created successfully!")
        return redirect('login')

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

            UserLogin.objects.create(
                user=registration,
                timestamp=timezone.now(),
                success=login_success
            )

            if login_success:
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
            UserLogin.objects.create(
                user=None,
                timestamp=timezone.now(),
                success=False
            )
            messages.error(request, "No account found with that email.")

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

        registration = recovery_entry.user
        registration.password = make_password(new_password)
        registration.save()

        recovery_entry.delete()

        messages.success(request, "Your password has been reset successfully.")
        return redirect('login')

    return render(request, 'accounts/recover_form.html', {'token': token})


# -------------------------------
# 💖 Wishlist Views
# -------------------------------


@csrf_exempt
@require_POST
def add_to_wishlist(request):
    try:
        print("RAW BODY:", request.body)

        data = json.loads(request.body)
        print("PARSED DATA:", data)

        first_name = data.get("user_first_name")
        product_id = data.get("product_id")
        product_name = data.get("product_name")
        product_image = data.get("product_image")

        if not all([first_name, product_id, product_name, product_image]):
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        # Find the most recent successful login for this user
        user_login = UserLogin.objects.filter(
            user__first_name=first_name,
            success=True
        ).order_by('-timestamp').first()

        if not user_login:
            return JsonResponse({"success": False, "error": "User login not found"}, status=404)

        # Prevent duplicates
        exists = WishlistItem.objects.filter(
            user_login=user_login,
            product_id=product_id
        ).exists()

        if exists:
            return JsonResponse({"success": False, "error": "Item already in wishlist 💫"}, status=200)

        WishlistItem.objects.create(
            user_login=user_login,
            product_id=product_id,
            product_name=product_name,
            product_image=product_image
        )

        return JsonResponse({
            "success": True,
            "status": "added",
            "message": f"{product_name} added to wishlist 💖"
        })
    except Exception as e:
        print("ERROR:", str(e))
        return JsonResponse({"success": False, "error": str(e)}, status=400)




@csrf_exempt
@require_POST
def view_wishlist(request):
    items = WishlistItem.objects.filter(user_login=request.user.userlogin)
    return render(request, "wishlist.html", {"items": items})


@csrf_exempt
@require_POST
def wishlist_drawer(request):
    items = WishlistItem.objects.filter(user_login=request.user.userlogin)
    return render(request, "partials/wishlist_drawer.html", {"items": items})


@csrf_exempt
@require_POST
def get_wishlist(request):
    try:
        user_login = UserLogin.objects.filter(
            user__email=request.user.email,
            success=True
        ).order_by("-timestamp").first()

        if not user_login:
            return JsonResponse({"status": "error", "message": "UserLogin not found"}, status=404)

        items = list(
            WishlistItem.objects.filter(user_login=user_login)
            .values("product_id", "product_name", "product_image")
        )
        return JsonResponse({"status": "success", "items": items})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


# -------------------------------
# 🚪 Logout View
# -------------------------------

def logout_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            user_login = UserLogin.objects.filter(
                user__email=user.email,
                success=True
            ).order_by("-timestamp").first()
            if user_login:
                LogoutEvent.objects.create(user_login=user_login)
        except Exception:
            pass
    django_logout(request)
    return redirect('/')




