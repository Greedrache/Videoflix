from django.urls import path

from . import views

urlpatterns = [
    path("video/", views.year_archive),
    path("video/<int:movie_id>/<str:resolution>/index.m3u8", views.month_archive),
    path("video/<int:movie_id>/<str:resolution>/<str:segment>/", views.article_detail),
]