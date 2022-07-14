from rest_framework import serializers
from lannister_auth .models import LannisterUser


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LannisterUser
        fields = "__all__"

