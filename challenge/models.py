from django.db import models
from user_task.models import Task
from django.contrib.auth import get_user_model
from user.models import Company
from django.utils import timezone

User = get_user_model()


class Challenge(models.Model):
    company = models.ForeignKey(
        Company,
        related_name="company_challenges",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
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
    challenge_expiry_time = models.DateTimeField()
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name
    
    def is_company_challenge(self):
        return self.company != None
    
    def is_active(self):
        now = timezone.now()
        return now > self.challenge_expiry_time


class TaskChallenge(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.CASCADE,
    )
    task_max_limit = models.PositiveIntegerField(
        default=3,
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
    points = models.PositiveIntegerField(
        default=0
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
    )
    last_updated = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.user)
