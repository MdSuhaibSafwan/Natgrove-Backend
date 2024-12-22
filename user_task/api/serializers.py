from rest_framework import serializers
from ..models import Task, TaskCategory, TaskImpact, CO2Saved, SDG, UserTask, UserTaskReward, UserTaskFile, UserTaskBookmark
from user.api.serializers import UserPublicProfileSerializer
from challenge.models import TaskChallenge
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class UserTaskBookmarkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    task = serializers.SerializerMethodField()
    task_id = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = UserTaskBookmark
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        try:
            obj = super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(e)

        return obj
    
    def get_task(self, obj):
        serializer = TaskSerializer(obj.task, context={"request": self.context.get("request")})
        return serializer.data


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

    def validate(self, attrs):
        task = attrs["task"]
        request = self.context.get("request")
        is_challenge = hasattr(attrs, "challenge")
        if is_challenge:
            times_user_took_challenge = UserTask.objects.filter(
                challenge=challenge,
                user=request.user,
                task=task,
                is_active=True,
            ).count()
            challenge = getattr(attrs, "challenge")
            task_challenge = TaskChallenge.objects.get(
                challenge=challenge,
                task=task,
            )
            if task_challenge.task_max_limit <= times_user_took_challenge:
                raise serializers.ValidationError("Already max limit reached for the challenge")

        else:
            times_user_took_challenge = UserTask.objects.filter(
                is_active=True,
                challenge=None,
                user=request.user,
                task=task,
            ).count()
            if task.max_limit_complete <= times_user_took_challenge:
                raise serializers.ValidationError("Max Limit reached for task")


        return super().validate(attrs)

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
        self.new_instance_created = True
        return obj

    def will_show_coin_reward(self, instance):
        task = instance.task
        challenge = instance.challenge
        if challenge:
            return True

        if not task.is_verification_required:
            return True

        return False


    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        data.update({
            "show_coin": False
        })
        new_instance_created = getattr(self, "new_instance_created", None)
        if new_instance_created:
            data["show_coin"] = self.will_show_coin_reward(instance)

        return data