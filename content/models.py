from django.db import models

# Create your models here.

class Video(models.Model):
    """
    Model representing a video in the Videoflix application. This model includes fields for title, description, release date, and genre.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title