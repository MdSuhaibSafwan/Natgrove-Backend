from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path("api/user/", include("user.api.urls")),
    path("api/", include("user_task.api.urls")),
    path("api/", include("feed.api.urls")),
    path("api/", include("challenge.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
