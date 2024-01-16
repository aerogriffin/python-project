import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .filters import brightness_filter, slow_motion_filter, mirror_filter, rotate_filter, black_and_white_filter, invert_colors_filter, substitute_face, apply_super_resolution
from .forms import VideoUploadForm
from .models import UserProfile, Video


def home(request):
    return render(request, "main/home.html")


def video_list(request):
    user_profiles = UserProfile.objects.all()
    return render(request, "main/video_list.html", {"user_profiles": user_profiles})


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


@login_required
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


def view_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "main/view_video.html", {"video": video})


@login_required
def apply_filter(request, video_id, filter_type):
    if request.method != "POST":
        return redirect("error-page")

    original_video = get_object_or_404(Video, id=video_id)
    original_video_path = original_video.video_file.path
    original_video_title = os.path.splitext(os.path.basename(original_video_path))[0]
    extension = os.path.splitext(os.path.basename(original_video_path))[1]

    if filter_type == "increase_brightness":
        processed_clip = brightness_filter(original_video_path, factor=1.5)
    elif filter_type == "decrease_brightness":
        processed_clip = brightness_filter(original_video_path, factor=0.5)
    elif filter_type == "slow_motion_effect":
        processed_clip = slow_motion_filter(original_video_path, factor=0.5)
    elif filter_type == "speed-up_effect":
        processed_clip = slow_motion_filter(original_video_path, factor=1.5)
    elif filter_type == "mirror":
        processed_clip = mirror_filter(original_video_path)
    elif filter_type == "rotate":
        processed_clip = rotate_filter(original_video_path, angle=180)
    elif filter_type == "blackwhite":
        processed_clip = black_and_white_filter(original_video_path)
    elif filter_type == "invert_colors":
        processed_clip = invert_colors_filter(original_video_path)
    elif filter_type == "substitute_face":
        processed_clip = substitute_face(original_video_path, substitute_image_path='/home/tec_web/Escritorio/python-project-main/main/face_photo.jpg')
    elif filter_type == "super_resolution":
        processed_clip = apply_super_resolution(original_video_path)

    processed_video_filename = f"{original_video_title}_{filter_type}{extension}"
    processed_video_path = os.path.join(os.path.dirname(original_video_path), processed_video_filename)
    processed_clip.write_videofile(processed_video_path)

    new_video_title = f"{original_video_title} {filter_type}"
    new_video = Video(title=new_video_title, video_file=processed_video_path)
    new_video.save()
    video_url = f"http://localhost:8000/videos/{processed_video_filename}"
    return redirect(video_url)


"""def download_video(request, video_id):
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
        return HttpResponse(f"Error: {e!s}", status=500)"""
