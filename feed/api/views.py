from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .serializers import UserPostSerializer, PostReactSerializer, PostCommentSerializer
from django.contrib.auth import get_user_model
from ..utils import get_user_feed
from .permissions import IsAuthenticated
from ..models import UserPost, PostComment, PostReact
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class FeedListAPIView(ListAPIView):
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = get_user_feed(self.request.user)
        return qs


class UserPostModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserPostSerializer

    def get_queryset(self):
        qs = UserPost.objects.all()
        return qs

    @action(methods=["POST", ], detail=True, url_path="comment")
    def comment_on_post(self, *args, **kwargs):
        serializer = PostCommentSerializer(
            data=self.request.data
        )
        serializer.context.update({
            "request": self.request,
            "post": self.get_object(),
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST", ], detail=True, url_path="react")
    def react_on_post(self, *args, **kwargs):
        serializer = PostReactSerializer(
            data=self.request.data
        )
        serializer.context.update({
            "request": self.request,
            "post": self.get_object(),
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

