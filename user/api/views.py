from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserEditProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]  

    def get_object(self):
        return self.request.user


class UserProfileAPIView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


@permission_classes([IsAuthenticated, ])
@api_view(["POST", ])
def deactivate_account(request, *args, **kwargs):
    user = request.user
    user.is_active = False
    user.save()
    data = {
        "message": "account deactivated"
    }
    return Response(data, status=status.HTTP_200_OK)
