from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import UserLoginSerializer, UserRegisterSerializer, UserProfileSerializer, UserChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

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


class ChangePasswordAPIView(APIView):
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.context.update({
            "request": request
        })
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        data = {
            "message": "Password Changed",
        }
        return Response(data, status=status.HTTP_200_OK)


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


@permission_classes([IsAuthenticated, ])
@api_view(["GET", ])
def get_content_for_app(request, *args, **kwargs):
    q = request.query_params.get("q", None)
    if q is None:
        raise NotFound("Parameter q not found")
    
    if q == "about-us":
        content = "About us content"

    elif q == "terms-and-conditions":
        content = "terms-and-conditions content"

    elif q == "privacy-policy":
        content = "privacy-policy content"
    
    else:
        raise NotFound("Didn't provide good q parameter")

    data = {
        "content": content,
    }
    return Response(data, status=status.HTTP_200_OK)
