from rest_framework import serializers
from lannister_slack.models import BonusRequest


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = BonusRequest

