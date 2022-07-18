from rest_framework import serializers
from lannister_auth .models import LannisterUser
from lannister_requests .models import BonusRequest


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LannisterUser
        fields = "__all__"


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = "__all__"
