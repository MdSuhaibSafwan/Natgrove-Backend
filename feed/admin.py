from django.contrib import admin
from .models import UserPost, PostReact, PostComment

admin.site.register(UserPost)
admin.site.register(PostReact)
admin.site.register(PostComment)

