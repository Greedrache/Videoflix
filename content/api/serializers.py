from rest_framework import serializers
from content.models import Video



class VideoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()
    category = serializers.CharField(max_length=100)

    class Meta:
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']

