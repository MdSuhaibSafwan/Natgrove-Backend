# Generated by Django 4.0.1 on 2024-12-15 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reward', '0004_giftvoucher_company_reward_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftvoucher',
            name='company_reward',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reward.companyreward'),
        ),
        migrations.AlterField(
            model_name='productcard',
            name='company_reward',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reward.companyreward'),
        ),
    ]
