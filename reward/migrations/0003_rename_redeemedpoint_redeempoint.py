# Generated by Django 4.0.1 on 2024-12-15 18:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reward', '0002_companyreward_productcard_remove_giftvoucher_company_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RedeemedPoint',
            new_name='RedeemPoint',
        ),
    ]
