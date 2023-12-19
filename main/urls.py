from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("upload/", views.upload_video, name="upload_video"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("account/profile/", views.account_profile, name="account_profile"),
]
