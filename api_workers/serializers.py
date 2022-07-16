from rest_framework import serializers
from lannister_auth .models import LannisterUser


class WorkerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LannisterUser
        fields = ["id", "username", "email", "first_name", "last_name", "roles"]
        read_only_fields = ["id", "roles"]


class WorkerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LannisterUser
        fields = ["id", "username", "email", "first_name", "last_name", "roles"]
        read_only_fields = ["id"]



