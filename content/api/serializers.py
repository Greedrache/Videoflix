from rest_framework import serializers
from content.models import Video

class VideoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Video model. Converts Video instances to and from JSON format for API responses and requests.
    """
    class Meta:
        model = Video
        fields = '__all__' 