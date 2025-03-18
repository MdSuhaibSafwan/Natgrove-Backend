from django.shortcuts import render
from django.conf import settings


def index(request):
    print(settings.DATABASES)
    return render(request, "index.html")
