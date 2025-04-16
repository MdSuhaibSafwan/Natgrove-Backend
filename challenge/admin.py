from django.contrib import admin
from .models import Challenge, TaskChallenge, UserChallengeJoining, ChallengeImage


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ["id", ]


admin.site.register(Challenge)
admin.site.register(TaskChallenge)
admin.site.register(UserChallengeJoining)
admin.site.register(ChallengeImage)
