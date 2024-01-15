import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from moviepy.editor import VideoFileClip

from .forms import VideoUploadForm
from .models import UserProfile, Video
from .videoutils import apply_slow_motion_effect, apply_color_filter, apply_grayscale_filter, apply_vignette_filter, apply_blur_filter, apply_sharpen_filter, apply_contrast_enhancer_filter, apply_brightness_enhancer_filter, apply_face_detection


def home(request):
    return render(request, "main/home.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def upload_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save()
            request.user.userprofile.videos.add(video_instance)
            return redirect("/")
    else:
        form = VideoUploadForm()
    return render(request, "main/upload.html", {"form": form})

def apply_filter(request, video_id, filter_type):
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.path

    output_path = f"media/filtered_videos/{request.user.username}_filtered.mp4"  

    if filter_type == 'slow_motion':
        apply_slow_motion_effect(video_path, output_path, factor=0.5)
    elif filter_type == 'color_filter':
        apply_color_filter(video_path, output_path, color="sepia")
    elif filter_type == 'grayscale_filter':
        apply_grayscale_filter(video_path, output_path)
    elif filter_type == 'vignette_filter':
        apply_vignette_filter(video_path, output_path, strength=0.5)
    elif filter_type == 'blur_filter':
        apply_blur_filter(video_path, output_path, radius=5)
    elif filter_type == 'sharpen_filter':
        apply_sharpen_filter(video_path, output_path, amount=1.5)
    elif filter_type == 'contrast_enhancer_filter':
        apply_contrast_enhancer_filter(video_path, output_path, factor=1.5)
    elif filter_type == 'brightness_enhancer_filter':
        apply_brightness_enhancer_filter(video_path, output_path)
    elif filter_type == 'face_detection_filter':
        apply_face_detection(video_path, output_path)

    template_path = os.path.join('main', 'filter_result.html')
    return render(request, template_path, context={'filtered_video_path': output_path})

def account_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={"username": user.username, "email": user.email},
    )
    user_videos = user_profile.videos.all()
    return render(
        request,
        "main/account_profile.html",
        {"username": user_profile.username, "email": user_profile.email, "user_videos": user_videos},
    )


def result(request, video_id):
    # Aquí puedes procesar el video y mostrar el resultado
    video = Video.objects.get(id=video_id)
    return render(request, "video_filter/result.html", {"video": video})


def download_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Ruta del archivo de video original
    original_video_path = video.video_file.path

    # Ruta del archivo de video convertido a MP4
    mp4_video_path = original_video_path.replace(os.path.splitext(original_video_path)[1], ".mp4")

    try:
        # Si el archivo no ha sido convertido a MP4, intenta hacerlo
        if not os.path.exists(mp4_video_path):
            clip = VideoFileClip(original_video_path)
            clip.write_videofile(mp4_video_path, codec="libx264", audio_codec="aac")

        # Abre el archivo convertido en modo binario
        with open(mp4_video_path, "rb") as video_file:
            # Crea la respuesta HTTP con el contenido del archivo
            response = HttpResponse(video_file.read(), content_type="video/mp4")
            # Configura el encabezado para forzar la descarga del archivo con un nombre específico
            response["Content-Disposition"] = f'attachment; filename="{video.title}.mp4"'
            return response
    except Exception as e:
        # Manejar cualquier error durante la conversión o lectura del archivo
        return HttpResponse(f"Error: {e!s}", status=500)


def video_list(request):
    user_profiles = UserProfile.objects.all()
    return render(request, "main/video_list.html", {"user_profiles": user_profiles})
