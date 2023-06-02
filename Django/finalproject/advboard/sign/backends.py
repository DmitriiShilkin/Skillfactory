from django.contrib.auth.models import User

from .models import OneTimeCode


class OneTimeCodeBackend(object):
    def authenticate(self, code):
        if not code:
            return None
        try:
            otcode = OneTimeCode.objects.get(pk=code)
        except OneTimeCode.DoesNotExist:
            return None
        user = otcode.user
        otcode.delete()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
