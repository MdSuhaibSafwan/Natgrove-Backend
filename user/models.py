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
    )
    company = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
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
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class UserPost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        "user_task.UserTask",
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.id)


class PostReact(models.Model):
    POST_REACT_TYPE = [
        ["L", "Like"],
        ["H", "Heart"],
        ["HAHA", "HAHA"],
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        UserPost,
        on_delete=models.CASCADE,
    )
    react_type = models.CharField(
        max_length=4,
        choices=POST_REACT_TYPE
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = [["user", "post"], ]
        ordering = ["-date_created", ]

    def __str__(self):
        return str(self.id)


class PostComment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        UserPost,
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.id)
