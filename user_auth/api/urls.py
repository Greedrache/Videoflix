from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name='register'),
    path("login/", views.login_user, name='login'),
    path("activate/<uidb64>/<token>/", views.activate_user, name='activate'),
    path("logout/", views.logout_user, name='logout'),
    path("token/refresh/", views.refresh_token, name='token_refresh'),
    path("password_reset/", views.password_reset_request, name='password_reset'),
    path("password_confirm/<uidb64>/<token>/", views.password_reset_confirm, name='password_reset_confirm'),
]
