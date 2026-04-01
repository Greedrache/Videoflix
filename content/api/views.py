from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models import Video
from .serializers import VideoSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def video_list(request):
    """
    View to list all videos or create a new video. This view handles GET requests to retrieve a list of all videos and POST requests to create a new video entry in the database.
    """
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


from django.http import FileResponse, Http404
import os
from django.conf import settings

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_video(request, movie_id, resolution):
    file_path = os.path.join(settings.MEDIA_ROOT, 'videos', str(movie_id), resolution, 'index.m3u8')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/vnd.apple.mpegurl')
        response['Cache-Control'] = 'no-cache'

        return response
    raise Http404("Video Playlist nicht gefunden.")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stream_video_segment(request, movie_id, resolution, segment):
    file_path = os.path.join(settings.MEDIA_ROOT, 'videos', str(movie_id), resolution, segment)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='video/MP2T')
        response['Cache-Control'] = 'max-age=3600'

        return response
    raise Http404("Video Segment nicht gefunden.")