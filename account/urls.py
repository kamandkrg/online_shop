from django.urls import path

from account.views import sing_up, login_user, logout_user, profile

urlpatterns = [
    path('login/', login_user, name="login"),
    path('register/', sing_up, name="register"),
    path('logout/', logout_user, name="logout"),
    path('profile/', profile, name="profile"),
]