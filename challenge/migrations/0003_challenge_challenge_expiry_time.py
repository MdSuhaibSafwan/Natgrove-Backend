# Generated by Django 4.0.1 on 2024-12-01 17:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0002_challenge_company_userchallengejoining_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='challenge_expiry_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]