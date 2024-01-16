from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
from .views import result, download_video, apply_filter


urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("register/", views.register, name="register"),
    path("upload/", views.upload_video, name="upload_video"),
    path("account/profile/", views.account_profile, name="account_profile"),
    path("resultado/<int:video_id>/", result, name="result"),
    path("download/<int:video_id>/", download_video, name="download_video"),
    path('video_list/', views.video_list, name='video_list'),
    path('apply_filter/<int:video_id>/<str:filter_type>/', apply_filter, name='apply_filter'),
    
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
