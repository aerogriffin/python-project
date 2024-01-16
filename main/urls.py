from django.conf import settings
from django.conf.urls.static import static
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
    path("video_list/", views.video_list, name="video_list"),
    path("apply_filter/<int:video_id>/<str:filter_type>/", views.apply_filter, name="apply_filter"),
    path("view_video/<int:video_id>/", views.view_video, name="view_video"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
