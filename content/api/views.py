from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Video
from .serializers import VideoSerializer

@api_view(['GET', 'POST'])
def video_list(request):
    """
    View to list all videos or create a new video. This view handles GET requests to retrieve a list of all videos and POST requests to create a new video entry in the database.
    """
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Beim ModelSerializer des DRF sind Dateien automatisch in request.data vorhanden, 
        # wir müssen KEIN separates 'files' Keyword-Argument übergeben.
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


