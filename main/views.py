from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import RegistrationForm, VideoUploadForm
from .models import UserProfile


def home(request):
    return render(request, "main/home.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "registration/login.html", {"error": "Invalid username or password"})
    else:
        return render(request, "registration/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def upload_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = VideoUploadForm()
    return render(request, "main/upload.html", {"form": form})


def account_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={"username": user.username, "email": user.email},
    )
    return render(
        request,
        "main/account_profile.html",
        {"username": user_profile.username, "email": user_profile.email},
    )
