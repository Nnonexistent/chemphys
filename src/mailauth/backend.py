from django.contrib.auth import get_user_model

from mailauth.models import MailAuthToken


# TODO: define abstract User model with unique email to use with mailauth app

class MailAuthBackend(object):
    def authenticate(self, mail_key=None):
        try:
            token = MailAuthToken.objects.get(key=mail_key)
        except MailAuthToken.DoesNotExist:
            return
        else:
            user, new = get_user_model().objects.get_or_create(email=token.email)
            token.delete()
            return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
