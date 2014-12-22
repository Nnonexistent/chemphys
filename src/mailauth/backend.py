from mailauth.models import MailAuthToken


class MailAuthBackend(object):
    def authenticate(self, token=None):
        try:
            MailAuthToekn.objects.get()
        except MailAuthToken.DoesNotExist:
            return