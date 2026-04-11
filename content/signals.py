from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .tasks import convert_to_hls_480p, convert_to_hls_720p, convert_to_hls_1080p, generate_thumbnail
from .models import Video
import os
import django_rq



@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for the post_save signal of the Video model. This function is called whenever a Video instance is saved. If a new Video instance is created, it triggers the conversion of the uploaded video file to HLS format with 480p resolution by calling the convert_to_hls_480p function as a background task using django-rq.
    """
    print('Signal received for Video model')
    if created:
         print('New object created')
         queue = django_rq.get_queue('default', autocommit=True)
         queue.enqueue(convert_to_hls_480p, instance.video_file.path, instance.id)
         queue.enqueue(convert_to_hls_720p, instance.video_file.path, instance.id)
         queue.enqueue(convert_to_hls_1080p, instance.video_file.path, instance.id)
         if not instance.thumbnail_url:
             queue.enqueue(generate_thumbnail, instance.video_file.path, instance.id)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Video` object is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)