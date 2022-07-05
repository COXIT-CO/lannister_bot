from rest_framework.serializers import ModelSerializer
from lannister_slack.models import BonusRequest


class BonusRequestSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = "__all__"
