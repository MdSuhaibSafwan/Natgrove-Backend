from rest_framework import viewsets
from ..models import Task, TaskCategory, TaskImpact, CO2Saved, SDG, UserTask, UserTaskReward
from django.contrib.auth import get_user_model
from . import serializers
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView
from ..utils import get_tasks_by_task_category, search_in_task_and_task_category
from . import pagination


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer
    pagination_class = pagination.TaskPagination

    def filter_queryset(self, queryset):
        # "Load more" button is needed in [home--chose-action--view-action]
        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = get_tasks_by_task_category(category_id, queryset)

        return queryset

    def get_queryset(self):
        qs = Task.objects.all()
        return qs


class TaskCategoryListAPIView(ListAPIView):
    serializer_class = serializers.TaskCategoryDetailSerializer
    pagination_class = pagination.TaskCategoryPagination

    def filter_queryset(self, queryset):
        search = self.request.query_params.get("search", None)
        if search:
            queryset = search_in_task_and_task_category(search)
        
        return queryset

    def get_queryset(self):
        qs = TaskCategory.objects.all()
        return qs


class UserTaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserTaskSerializer

    def get_queryset(self):
        queryset = UserTask.objects.filter(
            user=self.request.user,
        )
        return queryset
