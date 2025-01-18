from django.db import models

# django.contrib.auth.models

from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


class UserManager(BaseUserManager):

    def _create_user(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password):
        user = self._create_user(email, password)
        # user.is_superuser = True
        user.is_active = True
        # user.is_admin = True
        user.save()
        return user		

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_active = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [
        ["C", "COMPANY"],
        ["CU", "COMAPNY USER"],
        ["NU", "NORMAL USER"],
    ]
    email = models.EmailField(unique=True, )
    first_name = models.CharField(max_length=100, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=16, null=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    user_type = models.CharField(
        choices=USER_TYPE,
        max_length=2,
    )
    total_points = models.PositiveIntegerField(
        default=0
    )
    push_notifications = models.BooleanField(
        default=True,
    )

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.email

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    company = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
        null=True,
    )
    image = models.ImageField(
        default="user/images/default.webp",
        upload_to="user/images/"
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.user)


class Company(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=60,
    )
    description = models.TextField()
    profile_image = models.ImageField()
    is_verified = models.BooleanField(
        default=False,
    )
    logo = models.ImageField(
        upload_to="company/logo",
        null=True,
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


