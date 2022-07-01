from rest_framework.serializers import ModelSerializer
from lannister_auth.models import LannisterUser, Role


class UserSerializer(ModelSerializer):
    class Meta:
        ordering = ["id"]
        model = LannisterUser
        fields = "__all__"  # exclude some fields like password later


class RoleSerializer(ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Role
        fields = ["id", "users"]
