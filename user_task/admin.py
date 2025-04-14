from django.contrib import admin
from .models import SDG, TaskImpact, TaskCategory, CO2Saved, Task, UserTask, UserTaskBookmark, UserTaskReward, UserTaskFile

admin.site.register(SDG)
admin.site.register(TaskImpact)
admin.site.register(TaskCategory)
admin.site.register(CO2Saved)
admin.site.register(Task)
admin.site.register(UserTask)
admin.site.register(UserTaskFile)
admin.site.register(UserTaskBookmark)
admin.site.register(UserTaskReward)
