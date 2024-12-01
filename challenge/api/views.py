from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import ChallengeSerializer, ChallengeAddTaskSerializer
from ..models import Challenge
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        qs = Challenge.objects.all()
        return qs

    @action(methods=["POST", ], detail=True, url_path="add-tasks")
    def add_task_to_challenge_api_view(self, *args, **kwargs):
        obj = self.get_object()
        serializer = ChallengeAddTaskSerializer(data=self.request.data)
        serializer.context.update({
            "challenge": obj,
            "request": self.request,
        })
        serializer.is_valid(raise_exception=True)
        challenge = serializer.save()
        serializer = self.serializer_class(instance=challenge)
        data = {
            "message": "Tasks added",
            "data": serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @action(methods=["POST", ], detail=True, url_path="join-challenge")
    def join_challenge_api_view(self, *args, **kwargs):
        obj = self.get_object()
        serializer = ChallengeJoinSerializer(data=self.request.data)
        serializer.context.update({
            "challenge": obj,
            "request": self.request,
        })
        challenge = serializer.save()
        serializer = self.serializer_class(instance=challenge)
        data = {
            "message": "User Joined in challenge",
            "data": serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)

