from rest_framework.serializers import ModelSerializer
from lannister_slack.models import BonusRequest

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
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at',)

class BonusRequestRewieverSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = "__all__"
        read_only_fields = ('creator', 'reviewer', 'description', 'created_at', 'updated_at',)

class BonusRequestBaseSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = "__all__"
        read_only_fields = ('creator', 'created_at', 'updated_at', 'price_usd', 'payment_date', )
