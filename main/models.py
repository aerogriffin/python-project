from django.db import models


class Video(models.Model):
    video_file = models.FileField(upload_to="videos/")

    def __str__(self):
        return self.video_file.name
