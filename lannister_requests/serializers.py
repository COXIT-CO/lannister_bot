from rest_framework.serializers import ModelSerializer
from lannister_requests.models import BonusRequest, BonusRequestsHistory, BonusRequestStatus

#
# class BonusRequestSerializer(ModelSerializer):
#     class Meta:
#         model = BonusRequest
#         fields = "__all__"
#

"""
For per-field permissions(update method)
"""

class BonusRequestAdminSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = ['id', 'creator', 'reviewer', 'status', 'bonus_type', 'description', 'created_at', 'updated_at', 'price_usd', 'payment_date']
        read_only_fields = ('created_at', 'updated_at',)

class BonusRequestRewieverSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = ['id', 'creator', 'reviewer', 'status', 'bonus_type', 'description', 'created_at', 'updated_at', 'price_usd', 'payment_date']
        read_only_fields = ('creator', 'created_at', 'updated_at',)

class BonusRequestBaseSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = ['id', 'creator', 'reviewer', 'status', 'bonus_type', 'description', 'created_at', 'updated_at', 'price_usd', 'payment_date']
        read_only_fields = ('creator', 'status', 'created_at', 'updated_at', 'price_usd', 'payment_date',)

class BonusRequestHistorySerializer(ModelSerializer):
    class Meta:
        model = BonusRequestsHistory
        fields = ('status', 'updated_at',)
        read_only_fields = ('status', 'updated_at',)

class FullHistorySerializer(ModelSerializer):
    history_requests = BonusRequestHistorySerializer(many=True, read_only=True)
    class Meta:
        model = BonusRequest
        fields = ['id', 'creator', 'reviewer', 'bonus_type', 'price_usd', 'payment_date', 'history_requests']
        read_only_fields = ['id', 'creator', 'reviewer', 'bonus_type', 'price_usd', 'payment_date', 'history_requests']

class BonusRequestStatusSerializer(ModelSerializer):
    class Meta:
        model = BonusRequestStatus
        fields = "__all__"
