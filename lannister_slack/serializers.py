from rest_framework.serializers import ModelSerializer
from lannister_slack.models import BonusRequest
from lannister_auth.serializers import UserSerializer


class BonusRequestSerializer(ModelSerializer):
    creator = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)

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
        ]
