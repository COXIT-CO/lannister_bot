from rest_framework import serializers
from lannister_auth.models import LannisterUser
from lannister_roles.serializers import RoleSerializer


class WorkerSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = LannisterUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "slack_user_id",
            "slack_channel_id",
            "roles",
        ]
