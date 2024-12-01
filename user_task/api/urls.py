from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("tasks", views.TaskViewSet, "tasks")
router.register("user-task", views.UserTaskViewSet, "user-task")

urlpatterns = [
    path("tasks/categories/", views.TaskCategoryListAPIView.as_view(), ),
    path("", include(router.urls)),
]
