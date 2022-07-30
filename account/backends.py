from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

from account.models import User


class MyBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.filter(Q(username=username) | Q(email=username) | Q(phone=username)).first()
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
