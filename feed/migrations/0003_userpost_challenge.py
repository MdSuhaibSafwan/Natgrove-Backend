# Generated by Django 4.0.1 on 2025-05-18 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0006_challengeimage'),
        ('feed', '0002_rename_task_userpost_user_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='challenge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='challenge.challenge'),
        ),
    ]
