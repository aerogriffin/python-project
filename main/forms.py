from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator

from .models import Video


class LogInUsers(forms.Form):
    username = forms.CharField(label="User", max_length=10, widget=forms.TextInput(attrs={"placeholder": "user"}))
    password = forms.CharField(
        label="Password",
        max_length=20,
        widget=forms.PasswordInput(attrs={"placeholder": "password"}),
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email


class VideoUploadForm(forms.ModelForm):
    video_file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi"])])

    class Meta:
        model = Video
        fields = ["video_file"]
