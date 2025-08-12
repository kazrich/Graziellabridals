from .models import UserRegistration

def user_profile(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserRegistration.objects.get(user=request.user)
        except UserRegistration.DoesNotExist:
            pass
    return {'profile': profile}


