from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from panel.models import User


class AccountsBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            login_valid = True
        except User.DoesNotExist:
            user = None
            login_valid = False

        pwd_valid = check_password(password, user.password)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
