from django.contrib.auth.models import User
from django.db import models


class Video(models.Model):
    video_file = models.FileField(upload_to="videos/")

    def __str__(self):
        return self.video_file.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
