from rest_framework import serializers
from ..models import Challenge, UserChallengeJoining
from user_task.api.serializers import TaskSerializer, TaskImpactSerializer
from user_task.models import Task, TaskImpact
from user.api.serializers import UserPublicProfileSerializer


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
    is_user_already_joined = serializers.SerializerMethodField()
    challenge_percentage_completed = serializers.SerializerMethodField()
    challenge_impacts = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        exclude = [
            "users",
        ]

    def get_challenge_impacts(self, obj):
        tasks = obj.tasks.all()
        qs = TaskImpact.objects.filter(
            impact_tasks__in=tasks.values_list("id", flat=True)
        )
        serializer = TaskImpactSerializer(qs, many=True)
        return serializer.data

    def get_challenge_percentage_completed(self, obj):

        return float(50)

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
        request = self.context.get('request')
        qs = challenge.users.filter(users__id=request.user.id)
        if qs.exists():
            raise serializers.ValidationError("Already joined")
        
        return super().validate(attrs)

    def create(self, validated_data):        
        request = self.context.get('request')
        challenge = self.context.get("challenge")
        challenge.users.add(request.user)
        challenge.save()
        return challenge        
