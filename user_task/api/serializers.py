from rest_framework import serializers
from ..models import Task, TaskCategory, TaskImpact, CO2Saved, SDG, UserTask, UserTaskReward


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskCategoryDetailSerializer(serializers.ModelSerializer):
    categories_tasks = TaskSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = TaskCategory
        fields = "__all__"


class UserTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTask
        fields = "__all__"
