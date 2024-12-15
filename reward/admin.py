from django.contrib import admin
from .models import RedeemPoint, GiftVoucher, ProductCard, CompanyReward

admin.site.register(CompanyReward)
admin.site.register(GiftVoucher)
admin.site.register(ProductCard)
admin.site.register(RedeemPoint)
