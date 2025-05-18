from rest_framework import serializers
from ..models import Challenge, UserChallengeJoining, ChallengeImage
from user_task.api.serializers import TaskSerializer, TaskImpactSerializer, UserTaskFileSerializer
from user_task.models import Task, TaskImpact, UserTask, UserTaskFile
from user.api.serializers import UserPublicProfileSerializer
from feed.models import UserPost
from feed.api.serializers import UserPostSerializer


class ChallengeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChallengeImage
        exclude = [
            "challenge"
        ]


class UserTaskForChallengeDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    files_uploaded = UserTaskFileSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = UserTask
        fields = [
            "user",
            "files_uploaded",
            "description",
            "date_created"
        ]

    def get_user(self, obj):
        return f"{obj.user.get_full_name()}"


class UserChallengeJoiningSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(
        read_only=True,
    )

    class Meta:
        model = UserChallengeJoining
        fields = "__all__"


class ChallengeSerializer(serializers.ModelSerializer):
    total_user_joined = serializers.SerializerMethodField()
    is_user_already_joined = serializers.SerializerMethodField()
    challenge_percentage_completed = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        # fields = "__all__"
        exclude = [
            "users",
        ]

    def get_challenge_percentage_completed(self, obj):
        return float(50)

    def get_total_user_joined(self, obj):
        return obj.userchallengejoining_set.all().count()
        
    def get_is_user_already_joined(self, obj):
        request = self.context.get("request")
        qs = obj.users.filter(id=request.user.id)
        return qs.exists()


class ChallengeDetailSerializer(serializers.ModelSerializer):
    leaderboard = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    is_user_already_joined = serializers.SerializerMethodField()
    challenge_percentage_completed = serializers.SerializerMethodField()
    challenge_impacts = serializers.SerializerMethodField()
    images = ChallengeImageSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Challenge
        exclude = [
            "users",
        ]

    def get_challenge_impacts(self, obj):
        tasks = obj.tasks.all()
        qs = TaskImpact.objects.filter(
            impact_tasks__in=tasks.values_list("id", flat=True)
        ).distinct()
        serializer = TaskImpactSerializer(qs, many=True)
        return serializer.data

    def get_challenge_percentage_completed(self, obj):

        return float(50)

    def get_activities(self, obj):
        qs = UserPost.objects.filter(
            challenge=obj,
        )
        serializer = UserPostSerializer(qs, many=True)
        return serializer.data

    def get_leaderboard(self, obj):
        qs = obj.userchallengejoining_set.all().order_by("-points")
        serializer = UserChallengeJoiningSerializer(qs, many=True)
        return serializer.data
    
    def get_is_user_already_joined(self, obj):
        request = self.context.get("request")
        qs = obj.users.filter(id=request.user.id)
        return qs.exists()


class ChallengeAddTaskSerializer(serializers.Serializer):
    task_list = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
    )

    def create(self, validated_data):
        challenge = self.context.get("challenge")
        task_qs = Task.objects.filter(id__in=validated_data.get("task_list"))
        if not task_qs.exists():
            raise serializers.ValidationError("Tasks not found")

        for task in task_qs:
            challenge.tasks.add(task)

        challenge.save()
        return challenge


class ChallengeJoinSerializer(serializers.Serializer):

    def validate(self, attrs):
        challenge = self.context.get("challenge")
        request = self.context.get('request', None)
        if not request:
            raise serializers.ValidationError("request object not found")

        qs = challenge.users.filter(id=request.user.id)
        if qs.exists():
            raise serializers.ValidationError("Already joined")
        
        return super().validate(attrs)

    def create(self, validated_data):        
        request = self.context.get('request')
        challenge = self.context.get("challenge")
        challenge.users.add(request.user)
        challenge.save()
        return challenge        


class TaskForChallengeCompleteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    challenge = serializers.StringRelatedField(read_only=True)
    files = serializers.ListField(
        child=serializers.FileField(), 
        write_only=True,
    )
    files_uploaded = UserTaskFileSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = UserTask
        fields = "__all__"

    def create(self, validated_data):        
        request = self.context.get('request')
        challenge = self.context.get("challenge")
        validated_data["user"] = request.user
        validated_data["challenge"] = challenge

        files = validated_data.pop("files")
        obj = super().create(validated_data)

        for file in files:
            UserTaskFile.objects.create(
                user_task=obj,
                file=file
            )

        UserPost.objects.create(
            user_task=obj,
            user=request.user,
            challenge=challenge,
        )
        
        return obj
