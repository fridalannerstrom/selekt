from .models import Profile

def profile_picture(request):
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None
    else:
        profile = None

    return {'profile': profile}