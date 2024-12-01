from .models import UserPost
from user_task.models import UserTask


def get_user_feed(user):
    qs = UserPost.objects.filter(user=user)
    return qs
