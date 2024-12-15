# Generated by Django 4.0.1 on 2024-12-15 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_company_logo'),
        ('reward', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('points_required', models.PositiveIntegerField()),
                ('percentage', models.FloatField()),
                ('amount', models.FloatField()),
                ('gift_type', models.CharField(choices=[['CC', 'COUPON CARD'], ['GV', 'GIFT VOUCHER'], ['PC', 'PRODUCT CARD']], max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('product_data', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='giftvoucher',
            name='company',
        ),
        migrations.RemoveField(
            model_name='redeemedpoint',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='redeemedpoint',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='redeemedpoint',
            name='recipient_email',
        ),
        migrations.RemoveField(
            model_name='redeemedpoint',
            name='voucher',
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='greeting',
            field=models.CharField(default='hello', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='giftvoucher',
            name='recipient_email',
            field=models.EmailField(default='admin@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.DeleteModel(
            name='CouponCompany',
        ),
        migrations.AddField(
            model_name='redeemedpoint',
            name='reward',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reward.companyreward'),
        ),
    ]
