from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("posts", views.UserPostModelViewSet, basename="posts")

urlpatterns = [
    path("feed/", views.FeedListAPIView.as_view(), ),
    path("", include(router.urls)),
]
