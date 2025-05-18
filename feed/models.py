from django.db import models
from django.contrib.auth import get_user_model
from user_task.models import Task, UserTask

User = get_user_model()


class UserPost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    user_task = models.ForeignKey(
        "user_task.UserTask",
        on_delete=models.CASCADE,
    )
    challenge = models.ForeignKey(
        "challenge.Challenge",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
