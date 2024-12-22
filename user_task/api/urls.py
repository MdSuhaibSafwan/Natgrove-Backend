from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("tasks", views.TaskViewSet, "tasks")
router.register("user-task", views.UserTaskViewSet, "user-task")
router.register("task-bookmark", views.UserTaskBookmarkViewSet, basename="task-bookmark")

urlpatterns = [
    path("tasks/categories/", views.TaskCategoryListAPIView.as_view(), ),
    path("", include(router.urls)),
]
