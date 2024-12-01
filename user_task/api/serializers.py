from rest_framework import serializers
from ..models import Task, TaskCategory, TaskImpact, CO2Saved, SDG, UserTask, UserTaskReward, UserTaskFile
from user.api.serializers import UserPublicProfileSerializer


class TaskImpactSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskImpact
        fields = "__all__"

class UserTaskFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTaskFile
        fields = "__all__"


class CO2SavedSerializer(serializers.ModelSerializer):

    class Meta:
        model = CO2Saved
        fields = "__all__"
        

class TaskSerializer(serializers.ModelSerializer):
    co2_saved = CO2SavedSerializer(
        read_only=True
    )

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
    user = UserPublicProfileSerializer(
        read_only=True,
    )
    files_uploaded = UserTaskFileSerializer(
        read_only=True,
        many=True,
    )
    files = serializers.ListField(
        child=serializers.FileField(), 
        write_only=True,
    )

    class Meta:
        model = UserTask
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        files = validated_data.pop("files")
        obj = super().create(validated_data)
        for file in files:
            UserTaskFile.objects.create(
                user_task=obj,
                file=file
            )

        return obj
