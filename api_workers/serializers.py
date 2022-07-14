from rest_framework import serializers
from lannister_auth .models import LannisterUser


class WorkerBaseSerializer(serializers.ModelSerializer):
    class Meta:
        # extra_kwargs = {'password': {'write_only': True}, 'groups': {'write_only': True}, 'user_permissions': {'write_only': True}}
        model = LannisterUser
        fields = ["username", "email", "first_name", "last_name", "roles"]
        read_only_fields = ["roles"]


class WorkerAdminSerializer(serializers.ModelSerializer):
    class Meta:
        # extra_kwargs = {'password': {'write_only': True}, 'groups': {'write_only': True}, 'user_permissions': {'write_only': True}}
        model = LannisterUser
        fields = ["username", "email", "first_name", "last_name", "roles"]

