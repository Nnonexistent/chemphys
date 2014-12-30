from journal.models import LocalizedUser

def user(request):
    if hasattr(request, 'user') and request.user.is_authenticated():
        loc_user = LocalizedUser.objects.get(id=request.user.id)
    else:
        from django.contrib.auth.models import AnonymousUser
        loc_user = AnonymousUser()

    return {
        'loc_user': loc_user,
    }
