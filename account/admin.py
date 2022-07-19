from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'phone', 'username']


admin.site.register(User, CustomUserAdmin)
