from ..models import UserPost, PostComment, PostReact
from rest_framework import serializers
from user.api.serializers import UserPublicProfileSerializer
from user_task.api.serializers import UserTaskSerializer, TaskSerializer, CO2SavedSerializer
from user_task.models import UserTask, UserTaskFile


class UserTaskFileForFeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTaskFile
        fields = "__all__"


class UserTaskForFeedSerializer(serializers.ModelSerializer):
    files_uploaded = UserTaskFileForFeedSerializer(
        read_only=True, many=True,
    )

    class Meta:
        model = UserTask
        fields = "__all__"


class UserTaskDetailForFeedSerializer(serializers.ModelSerializer):
    files_uploaded = UserTaskFileForFeedSerializer(
        read_only=True, many=True,
    )
    task = TaskSerializer(
        read_only=True,
    )

    class Meta:
        model = UserTask
        fields = "__all__"



class UserPostSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(
        read_only=True,
    )
    user_task = UserTaskForFeedSerializer(
        read_only=True,
    )
    co2_saved = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = UserPost
        fields = "__all__"

    def get_co2_saved(self, obj):
        co2_saved = obj.user_task.task.co2_saved
        serializer = CO2SavedSerializer(co2_saved)
        return serializer.data
    
    def get_total_likes(self, obj):
        return obj.postreact_set.all().count()
    
    def get_total_comments(self, obj):
        return obj.postcomment_set.all().count()


class UserPostDetailSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(
        read_only=True,
    )
    user_task = UserTaskDetailForFeedSerializer(
        read_only=True,
    )

    class Meta:
        model = UserPost
        fields = "__all__"




class PostReactSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(
        read_only=True,
    )
    post = UserPostSerializer(
        read_only=True,
    )

    class Meta:
        model = PostReact
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        post = self.context.get("post")
        validated_data["user"] = request.user
        validated_data["post"] = post 
        return super().create(validated_data)


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(
        read_only=True,
    )
    post = UserPostSerializer(
        read_only=True,
    )

    class Meta:
        model = PostComment
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        post = self.context.get("post")
        validated_data["user"] = request.user
        validated_data["post"] = post
        return super().create(validated_data)
