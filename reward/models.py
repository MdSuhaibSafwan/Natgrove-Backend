from django.db import models
from challenge.models import Challenge
from user_task.models import Task
from lib.utils import get_base_model
from django.contrib.auth import get_user_model
from user.models import Company

BaseModel = get_base_model()
User = get_user_model()


class CompanyReward(BaseModel):
    GIFT_TYPE = [
        ["CC", "COUPON CARD"],
        ["GV", "GIFT VOUCHER"],
        ["PC", "PRODUCT CARD"],
    ]
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=200,
    )
    points_required = models.PositiveIntegerField()
    percentage = models.FloatField()
    amount = models.FloatField()
    gift_type = models.CharField(
        max_length=2, choices=GIFT_TYPE,
    )

    def __str__(self):
        return self.title


class ProductCard(BaseModel):
    company_reward = models.OneToOneField(
        CompanyReward,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    product_data = models.JSONField(default=dict)

    def __str__(self):
        return self.title


class GiftVoucher(BaseModel):
    company_reward = models.OneToOneField(
        CompanyReward,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=200,
    )
    description = models.TextField()
    amount = models.FloatField()
    points_required = models.PositiveIntegerField()
    recipient_email = models.EmailField()
    greeting = models.CharField(
        max_length=100,
    )
    message = models.TextField(
        null=True, blank=True,
    )
  
    def __str__(self):
        return self.title


class RedeemPoint(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    reward = models.ForeignKey(
        CompanyReward,
        on_delete=models.SET_NULL,
        null=True,
    )
    data = models.JSONField(
        default=dict,
    )

    def save(self, *args, **kwargs):
        if (self.voucher) and (self.coupon):
            raise ValueError("Cannot get voucher and coupon at same time")

        return super().save(*args, **kwargs)


"""
TYPES OF VOUCHERS,
1. SEND A GIFT,
2. GET IT FOR YOURSELF


"""
