from rest_framework import serializers
from lannister_auth.models import LannisterUser, Role


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_id_display")

    class Meta:
        model = Role
        fields = ("name",)


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
