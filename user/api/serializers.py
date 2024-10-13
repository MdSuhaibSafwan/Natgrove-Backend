from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        user_qs = User.objects.filter(
            email=email
        )
        if not user_qs.exists():
            raise serializers.ValidationError("Either Email or Password does not match")
        user = user_qs.get()
        password = attrs["password"]
        if not user.check_password(password):
            raise serializers.ValidationError("Password does not match")
            
        self.user = user
        return attrs

    def create(self, validated_data):
        token_obj, created = Token.objects.get_or_create(
            user=self.user,
        )
        self.token_obj = token_obj
        return token_obj

    @property
    def data(self):
        breakpoint()
        return self.token_obj.values()