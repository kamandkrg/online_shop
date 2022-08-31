from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class SuperUserPermission(BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class HaveUpdatePermission(BasePermission):
    message = 'you cant edit or see this user'

    def has_permission(self, request, view):
        user = User.objects.filter(id=request.GET.get('pk'))
        if (request.user == user) or request.user.is_superuser or request.user.is_staff:
            return True
        return False


class NotAuthenticatePermission(BasePermission):
    message = 'you are login'

    def has_permission(self, request, view):
        if request.user.is_anonymousor or request.user.is_superuser or request.user.is_staff:
            return True
        return False
