from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from lib.utils import get_base_model

User = get_user_model()
BaseModel = get_base_model()


class TaskImpact(BaseModel):
    title = models.CharField(
        max_length=100,
    )
    image = models.ImageField(
        upload_to="impact/badges",
    )

    def __str__(self):
        return self.title


class SDG(BaseModel):
    title = models.CharField(
        max_length=10,
    )
    image = models.ImageField(
        upload_to='sdg/images',
    )

    def __str__(self):
        return self.title


class CO2Saved(BaseModel):
    CO2_SAVED_CHOICES = [
        ["G", "GRAMS"],
        ["KG", "KILOGRAMS"]
    ]
    amount = models.FloatField()
    unit = models.CharField(
        max_length=2,
        choices=CO2_SAVED_CHOICES,
    )

    def __str__(self):
        return f"{self.amount}-{self.unit}"


class TaskCategory(BaseModel):
    title = models.CharField(
        max_length=60,
    )
    description = models.TextField(
        null=True, blank=True,
    )

    def __str__(self):
        return self.title


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
    co2_saved = models.ForeignKey(
        CO2Saved,
        on_delete=models.SET_NULL,
        null=True,
    )
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="categories_tasks",
    )
    sdgs = models.ManyToManyField(
        SDG,
        related_name="sdg_tasks",
    )
    impacts = models.ManyToManyField(
        TaskImpact,
        related_name="impact_tasks",
    )

    def __str__(self):
        return self.name


class UserTask(BaseModel):
    """
    THIS MODEL DEFINES THE TASK TAKEN BY A USER.
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_task",
    )
    challenge = models.ForeignKey(
        "challenge.Challenge",
        on_delete=models.SET_NULL,
        null=True,
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name="user_task_taken",
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    files_uploaded = models.FileField(
        upload_to="user-task/files/"
    )
    products_quantity = models.PositiveIntegerField(
        default=1,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_completed = models.BooleanField(
        default=False,
    )
    is_accepted = models.BooleanField(
        default=False,
    )
    reminder = models.DateTimeField(
        null=True,
        blank=True,
    )

    def is_challenge_task(self):
        return self.challenge != None

    def __str__(self):
        return str(self.task)


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
