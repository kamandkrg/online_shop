from django.urls import path, re_path

from user.views import login_email, login_username, login_number

urlpatterns = [
    re_path(r"login/(?P<email_login>[\w]+@[\w.]+$)", login_email),
    re_path(r"login/(?P<username_login>[\w])", login_username),
    re_path(r"login/(?P<number_login>[0-9]{11})", login_number)

]
