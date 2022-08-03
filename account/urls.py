from django.urls import path

from account.views import sing_up, login_user, logout_user

urlpatterns = [
    path('login/', login_user, name="login"),
    path('register/', sing_up, name="register"),
    path('logout/', logout_user, name="logout")
]