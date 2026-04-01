from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name='register'), #for registration
    path("login/", views.login_user, name='login'), #for login
    path("activate/<uidb64>/<token>/", views.activate_user, name='activate'), #for email verification
    path("logout/", views.logout_user, name='logout'), #for logout
    path("token/refresh/", views.refresh_token, name='token_refresh'), #for refreshing access token using refresh token
    path("password_reset/", views.password_reset_request, name='password_reset'), #for requesting password reset
    path("password_confirm/<uidb64>/<token>/", views.password_reset_confirm, name='password_reset_confirm'), #for confirming password reset and setting new password
]
