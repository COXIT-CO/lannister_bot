from rest_framework.serializers import ModelSerializer
from lannister_auth.models import LannisterUser


class UserSerializer(ModelSerializer):
    class Meta:
        ordering = ["id"]
        model = LannisterUser
        fields = "__all__"  # exclude some fields like password later
