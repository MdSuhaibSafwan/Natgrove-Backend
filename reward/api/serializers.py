from rest_framework import serializers
from ..models import CompanyReward, ProductCard, GiftVoucher, RedeemPoint


class ProductCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCard
        fields = "__all__"


class GiftVoucherSerializer(serializers.ModelSerializer):

    class Meta:
        model = GiftVoucher
        fields = "__all__"


# class ProductCardSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductCard
#         fields = "__all__"


class CompanyRewardSerializer(serializers.ModelSerializer):
    reward_type = serializers.CharField(
        write_only=True,
    )
    product_card = serializers.SerializerMethodField(
        method_name="get_product_card",
    )
    gift_voucher = serializers.SerializerMethodField(
        method_name="get_gift_voucher",
    )

    class Meta:
        model = CompanyReward
        fields = "__all__"

    def validate_reward_type(self, val):
        if val not in ["CC", "PC", "GV"]:
            raise serializers.ValidationError("Invalid reward_type")

        return val

    def get_product_card(self, obj):
        if not getattr(obj, "productcard", None):
            return None

        obj = obj.productcard
        context = {
            "request": self.context.get("request")
        }
        serializer = ProductCardSerializer(obj, context=context)
        return serializer.data

    def get_gift_voucher(self, obj):
        if not getattr(obj, "giftvoucher", None):
            return None

        obj = obj.giftvoucher
        context = {
            "request": self.context.get("request")
        }
        serializer = GiftVoucherSerializer(obj, context=context)
        return serializer.data


class RedeemRewardSerializer(serializers.Serializer):

    def validate(self, attrs):
        request = self.context.get("request", None)
        # check if user has points 

        return super().validate(attrs)

    def create(self, validated_data):
        request = self.context.get("request", None)
        if not request:
            raise serializers.ValidationError("No Request object found")
        
        reward = self.context.get("reward", None)
        obj = RedeemPoint(
            user=request.user,
            reward=reward,
        )
        obj.save()
        return obj
