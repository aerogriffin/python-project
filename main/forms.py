from django import forms
from django.core.validators import FileExtensionValidator

from .models import Video


class VideoUploadForm(forms.ModelForm):
    video_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi"])],
    )

    class Meta:
        model = Video
        fields = ["video_file"]


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "video_file"]
