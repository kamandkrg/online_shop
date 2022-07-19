from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, phone, password, **extra_fields):
        if not phone or not username or not email:
            raise ValueError("username, email and phone number must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, phone, password, **extra_fields)

    def create_superuser(self, username,  email, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, phone, password, **extra_fields)
