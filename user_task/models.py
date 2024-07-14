from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# from ClimateOClockBackend.utils import get_base_model

User = get_user_model()
# BaseModel = get_base_model()

class Task(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )
    name = models.CharField(
        max_length=15,
    )
    description = models.TextField()
    files = models.FileField(
        upload_to="task/files",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="task/image",
    )
    points = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class UserTaskReward(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="tasks",
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.SET_NULL,
        related_name="task_rewards",
    )
    description = models.TextField(
        null=True, 
        blank=True
    )

    def __str__(self):
        return str(self.user)

