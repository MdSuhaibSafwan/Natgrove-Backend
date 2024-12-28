from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from .models import Task, UserTask, UserTaskReward
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


@receiver(signal=pre_save, sender=UserTask)
def update_user_task_fields_if_created_according_to_verification_of_task(sender, instance, **kwargs):
    try:
        user_task = UserTask.objects.get(id=instance.id)    
    except ObjectDoesNotExist as e:
        user_task = None
        completed = False

    task = instance.task
    if user_task:
        completed = user_task.is_completed

    if not completed:
        if instance.is_completed == True:
            if task.is_verification_required == True:
                return False
            
            instance.is_accepted = True
            return instance

    return False


@receiver(signal=post_save, sender=UserTask)
def create_user_task_reward(sender, instance, created, **kwargs):
    if not created:
        qs = UserTaskReward.objects.filter(
            user=instance.user,
            user_task=instance,
        )
        if not qs.exists():
            task = instance.task
            if instance.is_accepted == True:
                obj = UserTaskReward.objects.create(
                    user=instance.user,
                    user_task=instance,
                )
                return obj
    
    if created:
        if instance.is_accepted == True:
            obj = UserTaskReward.objects.create(
                user=instance.user,
                user_task=instance,
            )
            return obj


@receiver(signal=post_save, sender=UserTaskReward)
def add_points_to_user_profile(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.total_points += instance.user_task.task.points
        user.save()
