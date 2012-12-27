from django.contrib.auth.backends import ModelBackend
from activebuys.apps.accounts.models import Account

class CustomBackend(ModelBackend):
    """ Auth backend for clients. """
    def authenticate(self, username=None, password=None):
        """
            Selecting user by 'name' then by 'email'.
            If found check password
        """
        user = None
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            pass
        if not user:
            try:
                user = Account.objects.get(email__iexact=username) # iexact
            except Account.DoesNotExist:
                pass
        if user and user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None