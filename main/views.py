from django.shortcuts import render


def home(request):
    return render(request, "main/base.html")


def members(request):
    return render(request, "main/members.html")
