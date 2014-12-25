from django.contrib.auth import get_user_model

from mailauth.models import MailAuthToken


class MailAuthBackend(object):
    def authenticate(self, mail_key=None):
        try:
            token = MailAuthToken.objects.get(key=mail_key)
        except MailAuthToken.DoesNotExist:
            return
        else:
            try:
                user = get_user_model().objects.filter(email=token.email).order_by('id')[0]
            except IndexError:
                username = token.email[:30]
                count = 1
                while get_user_model().objects.filter(username=username).exists():
                    count += 1
                    username = '%s_%s' % (username[:30-1-len(str(count))], count)
                user = get_user_model().objects.create(username=username, email=token.email)

                token.delete()
            return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None