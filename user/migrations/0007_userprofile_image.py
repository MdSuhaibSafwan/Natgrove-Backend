# Generated by Django 4.0.1 on 2025-01-18 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_push_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='user/images/default.webp', upload_to='user/images/'),
        ),
    ]
