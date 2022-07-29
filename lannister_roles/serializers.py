from rest_framework.serializers import ModelSerializer
from lannister_roles.models import Role


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = ["name", "description"]
        read_only_fields = ["name"]
