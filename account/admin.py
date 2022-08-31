
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User
from account.forms import UserCreationForm, UserChangeForm


class AccountAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'username', 'phone', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                    'is_active', 'sex', 'age')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'is_superuser', 'password', 'is_active')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'age', 'sex', 'email')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'is_superuser', 'is_active', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'age', 'sex', 'email')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'username', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, AccountAdmin)
