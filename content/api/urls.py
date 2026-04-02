from django.urls import path
from . import views


urlpatterns = [
     path("video/", views.video_list, name='video-list'), #for listing all videos and uploading new videos
     path("video/<int:movie_id>/<str:resolution>/index.m3u8", views.stream_video, name='stream-video'), #for streaming the video playlist (m3u8 file)
     path("video/<int:movie_id>/<str:resolution>/<str:segment>", views.stream_video_segment, name='stream-video-segment'), #for streaming individual video segments (ts files)
]