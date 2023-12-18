from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("members/", views.members, name="members"),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logOut, name='logout'),
]
