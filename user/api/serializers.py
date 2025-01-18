from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group, Permission
from ..models import UserProfile

User = get_user_model()


class UserGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class UserPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = "__all__"


class UserAchievementSerializer(serializers.ModelSerializer):
    average_co2_saved = serializers.SerializerMethodField()
    badges_earned = serializers.SerializerMethodField()
    user_impacts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["average_co2_saved", "badges_earned", "user_impacts"]

    def get_average_co2_saved(self, obj):

        return None

    def get_badges_earned(self, obj):

        return None

    def get_user_impacts(self, obj):

        return None


class UserActivitySerializer(serializers.ModelSerializer):
    point_history = serializers.SerializerMethodField()
    recent_posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["point_history", "recent_posts"]

    def get_point_history(self, obj):

        return None

    def get_recent_posts(self, obj):
        
        return None


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
    )
    password1 = serializers.CharField(
        write_only=True,
    )
    password2 = serializers.CharField(
        write_only=True,
    )

    def validate_old_password(self, val):
        request = self.context.get("request")
        user = request.user
        if not user.check_password(val):
            raise serializers.ValidationError("Entered Password didn't match your previous password")       
         
        return val

    def validate(self, attrs):
        password1 = attrs["password1"]
        password2 = attrs["password2"]
        if password1 != password2:
            raise serializers.ValidationError("Password Mismatch")
        
        return super().validate(attrs)

    def create(self, validated_data):
        new_password = validated_data.get("password1")
        request = self.context.get("request")
        user = request.user

        user.set_password(new_password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    is_active = serializers.ReadOnlyField()
    first_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    groups = UserGroupSerializer(read_only=True, many=True)
    user_permissions = UserPermissionSerializer(many=True, read_only=True)

    achievements = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password", "last_login", "is_superuser", "is_admin", "date_created", "last_updated"]

    def get_achievements(self, obj):
        serializer = UserAchievementSerializer(obj)
        serializer.context.update({"request": self.context.get("request")})
        return serializer.data

    def get_activities(self, obj):
        serializer = UserActivitySerializer(obj)
        serializer.context.update({"request": self.context.get("request")})
        return serializer.data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        # fields = "__all__"
        exclude = ["id", "user", ]


class UserPublicProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(
        read_only=True,
    )
    groups = UserGroupSerializer(read_only=True, many=True)
    user_permissions = UserPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ["password", "last_login", "is_superuser", "is_admin", "date_created", "last_updated"]


class RestTokenSerializer(serializers.ModelSerializer):
    user = UserPublicProfileSerializer(read_only=True)

    class Meta:
        model = Token
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ["last_login", "is_active", "is_superuser", "is_admin", "date_created", "last_updated"]
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_2"]:
            raise serializers.ValidationError("Password Mismatch")

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_2")
        password = validated_data.pop("password")
        user = User(
            **validated_data,
        )
        user.set_password(password)
        user.save()
        return user


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
            
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

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
        serializer = RestTokenSerializer(instance=self.token_obj)
        return serializer.data
