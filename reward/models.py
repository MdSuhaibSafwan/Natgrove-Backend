from django.db import models
from challenge.models import Challenge
from user_task.models import Task
from lib.utils import get_base_model
from django.contrib.auth import get_user_model

BaseModel = get_base_model()
User = get_user_model()


class CouponCompany(BaseModel):
    company_name = models.CharField(
        max_length=100,
    )
    company_logo = models.ImageField(
        upload_to="coupon/company/logo",
        null=True,
    )

    def __str__(self):
        return self.company_name


class GiftVoucher(BaseModel):
    company = models.ForeignKey(
        CouponCompany,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField()
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField()
    points_required = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Coupon(BaseModel):
    percentage = models.FloatField()
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title


class RedeemedPoint(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    voucher = models.ForeignKey(
        GiftVoucher,
        on_delete=models.SET_NULL,
        null=True,
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True
    )
    data = models.JSONField(
        default=dict,
    )
    recipient_email = models.EmailField()
    comment = models.TextField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if (self.voucher) and (self.coupon):
            raise ValueError("Cannot get voucher and coupon at same time")

        return super().save(*args, **kwargs)
