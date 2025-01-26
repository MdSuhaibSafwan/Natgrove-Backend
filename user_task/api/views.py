from rest_framework import viewsets
from ..models import Task, TaskCategory, TaskImpact, CO2Saved, SDG, UserTask, UserTaskReward, UserTaskBookmark
from django.contrib.auth import get_user_model
from . import serializers
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import ListAPIView
from ..utils import get_tasks_by_filtering, search_in_task_and_task_category
from . import pagination
from ..filters import UserTaskBookmarkFilter
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TaskSerializer
    pagination_class = pagination.TaskPagination
    classes_according_to_action = {
        "create": serializers.TaskSerializer,
        "list": serializers.TaskListSerializer,
        "retrieve": serializers.TaskDetailSerializer,
    }

    def get_serializer_class(self):
        try:
            serializer_class = self.classes_according_to_action[self.action]
        except Exception as e:
            print(e)
            return self.serializer_class
        
        return serializer_class

    def filter_queryset(self, queryset):
        # "Load more" button is needed in [home--chose-action--view-action]
        category_id = self.request.query_params.get("category_id")
        search = self.request.query_params.get("search")
        queryset = get_tasks_by_filtering(category_id, search, queryset)
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


class UserTaskBookmarkViewSet(viewsets.ModelViewSet):
    serializer_classes = {
        "create": serializers.UserTaskBookmarkSerializer,
    }
    default_serializer_class = serializers.TaskSerializer
    filter_backends = [UserTaskBookmarkFilter, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_serializer_class(self):
        serializer = self.serializer_classes.get(self.action, self.default_serializer_class)
        return serializer

    def get_queryset(self):
        return Task.objects.all()

    def filter_queryset(self, queryset):
        bookmark_queryset = UserTaskBookmark.objects.filter(
            user=self.request.user
        )
        q = self.request.query_params.get("q", None)
        if q:
            q = q.lower()
            if q != "completed":
                raise ValidationError("set 'q' to 'completed'")
            
            user_task_queryset = UserTask.objects.filter(
                user=self.request.user
            )
            queryset = Task.objects.filter(id__in=user_task_queryset.values_list("task__id", flat=True))
            return queryset

        queryset = Task.objects.filter(id__in=bookmark_queryset.values_list("task__id", flat=True))
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset


class UserContributionAPIView(APIView):

    def get(self, request, *args, **kwargs):
        serializer = serializers.UserTaskContributionSerializer(request.user, many=False)
        serializer.context.update({
            "request": request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)
