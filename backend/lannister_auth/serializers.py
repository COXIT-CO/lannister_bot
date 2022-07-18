from rest_framework.serializers import ModelSerializer
from lannister_auth.models import LannisterUser, Role


class UserSerializer(ModelSerializer):
    class Meta:
        ordering = ["id"]
        model = LannisterUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "slack_user_id",
            "roles",
        )


class RoleSerializer(ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Role
        fields = ["id", "users"]
