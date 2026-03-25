from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.year_archive),
    path("activate/<uidb64>/<token>/", views.month_archive),
    path("login/", views.article_detail),
    path("logout/", views.article_detail),
    path("token/refresh/", views.article_detail),
    path("password_reset/", views.article_detail),
    path("password_confirm/<uidb64>/<token>/", views.article_detail),
]