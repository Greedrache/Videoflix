from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Video
import os 



@receiver(post_save, sender=Video)
def create_lecture(sender, instance, created, **kwargs):
    print('Signal received for Video model')
    if created:
        print('New object created')


@receiver(post_delete, sender=Video)
def delete_lecture(sender, instance, **kwargs):
    """
    Signal receiver that deletes the video file from the filesystem when a Video instance is deleted.
    """
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)