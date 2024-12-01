from ..models import UserPost, PostComment, PostReact
from rest_framework import serializers
from user.api.serializers import UserPublicProfileSerializer
from user_task.api.serializers import UserTaskSerializer


class UserPostSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(
        read_only=True,
    )
    task = UserTaskSerializer(
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

