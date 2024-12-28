from django.dispatch import receiver
from .models import RedeemPoint
from django.db.models.signals import post_save


@receiver(signal=post_save, sender=RedeemPoint)
def cut_total_points_from_user(sender, intance, created, **kwargs):
    if created:
        user = instance.user
        points = instance.reward.points_required
        user.total_points = user.total_points - points
        user.save()
