from django.db import models
from user_task.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class Challenge(models.Model):
    users = models.ManyToManyField(
        User,
        related_name="user_challenges",
        through="UserChallengeJoining",
    )
    tasks = models.ManyToManyField(
        Task,
        related_name="task_challenges",
        through="TaskChallenge"
    )
    name = models.CharField(
        max_length=50,
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to="challenge/images",
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class TaskChallenge(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.task)


class UserChallengeJoining(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.user)
