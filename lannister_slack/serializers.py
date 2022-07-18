from rest_framework.serializers import ModelSerializer
from lannister_requests.models import (
    BonusRequest,
    BonusRequestStatus,
    BonusRequestsHistory,
)
from lannister_auth.serializers import UserSerializer


class BonusRequestStatusSerializer(ModelSerializer):
    class Meta:
        model = BonusRequestStatus
        fields = ("status_name",)


class BonusRequestSerializer(ModelSerializer):
    creator = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    status = BonusRequestStatusSerializer(read_only=True)

    class Meta:
        model = BonusRequest
        fields = [
            "id",
            "status",
            "bonus_type",
            "description",
            "created_at",
            "updated_at",
            "payment_date",
            "creator",
            "reviewer",
            "price_usd",
        ]


class BonusRequestHistory(ModelSerializer):
    bonus_request = BonusRequestSerializer()
    status = BonusRequestStatusSerializer()

    class Meta:
        model = BonusRequestsHistory
        fields = ["bonus_request", "status", "updated_at"]
