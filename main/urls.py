from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register, name="register"),
    path("upload/", views.upload_video, name="upload_video"),
    path("account/profile/", views.account_profile, name="account_profile"),
]
