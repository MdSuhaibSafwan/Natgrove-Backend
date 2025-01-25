from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import viewsets
from .serializers import UserPostSerializer, UserPostDetailSerializer, PostReactSerializer, PostCommentSerializer
from django.contrib.auth import get_user_model
from ..utils import get_user_feed
from .permissions import IsAuthenticated
from ..models import UserPost, PostComment, PostReact
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

User = get_user_model()


class FeedListAPIView(ListAPIView):
    serializer_class = UserPostSerializer
    permission_classes = []

    def get_queryset(self):
        qs = UserPost.objects.all()
        return qs


class FeedDetailAPIView(RetrieveAPIView):
    serializer_class = UserPostDetailSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        qs = UserPost.objects.all()
        return qs

    def get_object(self):
        qs = self.get_queryset()
        try:
            obj = qs.get(id=self.kwargs.get(self.lookup_url_kwarg))
        except UserPost.DoesNotExist as e:
            raise NotFound(e)

        return obj


class UserPostModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserPostSerializer

    def get_queryset(self):
        qs = UserPost.objects.all()
        return qs

    @action(methods=["PATCH", ], detail=True, url_path="comment")
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

    @action(methods=["PATCH", ], detail=True, url_path="react")
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

