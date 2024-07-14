from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from lib.utils import get_base_model

User = get_user_model()
BaseModel = get_base_model()

class Task(BaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
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


class UserTaskReward(BaseModel):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_task_reward",
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name="rewards",
    )
    description = models.TextField(
        null=True, 
        blank=True
    )

    def __str__(self):
        return str(self.user)

