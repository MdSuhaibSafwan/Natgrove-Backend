# Generated by Django 4.0.1 on 2024-12-22 14:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_task', '0010_taskbookmark'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaskBookmark',
            new_name='UserTaskBookmark',
        ),
        migrations.AlterUniqueTogether(
            name='usertaskbookmark',
            unique_together={('task', 'user')},
        ),
    ]