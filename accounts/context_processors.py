from accounts.models import UserRegistration

def user_profile(request):
    profile = None
    if request.user.is_authenticated and isinstance(request.user, UserRegistration):
        profile = request.user  # Already a UserRegistration instance
    return {'profile': profile}
