from rest_framework.viewsets import ModelViewSet
from . import serializers
from ..models import CompanyReward, ProductCard, GiftVoucher, RedeemPoint
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action


class CompanyRewardModelViewSet(ModelViewSet):
    serializer_class = serializers.CompanyRewardSerializer
    
    def get_queryset(self):
        qs = CompanyReward.objects.all()
        return qs

    @action(methods=["POST", ], detail=True, url_path="redeem-reward")
    def redeem_reward(self, *args, **kwargs):
        obj = self.get_object()
        context = {
            "request": self.request,
            "reward": obj,
        }
        serializer = serializers.RedeemRewardSerializer(data=self.request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": "Redeem Successful",
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
