from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserPost
from user_task.models import UserTask


@receiver(signal=post_save, sender=UserTask)
def add_user_post_for_user_task(sender, instance, created, **kwargs):
    if created:
        if not instance.is_accepted:
            return False
        
        UserPost.objects.create(
            user=instance.user,
            user_task=instance,
        )
