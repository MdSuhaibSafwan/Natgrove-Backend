# Generated by Django 4.0.1 on 2024-11-29 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0002_challenge_company_userchallengejoining_points'),
        ('user_task', '0002_co2saved_sdg_taskcategory_taskimpact_usertask_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertask',
            name='challenge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='challenge.challenge'),
        ),
    ]
