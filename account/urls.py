from django.urls import path

from account.views import sing_up, login_user, logout_user, profile, UpdatePasswordUserAPIView, UpdateUserAPIView, \
    SingUpAPIView, BlacklistRefreshView

urlpatterns = [
    path('login/', login_user, name="login"),
    path('register/', sing_up, name="register"),
    path('logout/', logout_user, name="logout"),
    path('profile/', profile, name="profile"),
    path('api/change-password/', UpdatePasswordUserAPIView.as_view(), name="change-password"),
    path('api/change-password/<int:pk>/', UpdatePasswordUserAPIView.as_view(), name="change-password-admin"),
    path('api/update/', UpdateUserAPIView.as_view(), name="edit"),
    path('api/update/<int:pk>/', UpdateUserAPIView.as_view(), name="edit-admin"),
    path('api/register/', SingUpAPIView.as_view(), name="register"),
    path('api/logout/', BlacklistRefreshView.as_view(), name="logout"),
]