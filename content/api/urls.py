from django.urls import path
from . import views


urlpatterns = [
     path("video/", views.video_list, name='video-list'),
     path("video/<int:movie_id>/<str:resolution>/index.m3u8", views.stream_video, name='stream-video'),
     path("video/<int:movie_id>/<str:resolution>/<str:segment>", views.stream_video_segment, name='stream-video-segment'),
]