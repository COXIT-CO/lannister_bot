from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from lannister_requests.models import (
    BonusRequest,
    BonusRequestsHistory,
    BonusRequestStatus,
)


class BonusRequestAdminSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class BonusRequestRewieverSerializer(ModelSerializer):
    class Meta:
        model = BonusRequest
        fields = "__all__"
        read_only_fields = (
            "creator",
            "reviewer",
            "description",
            "created_at",
            "updated_at",
        )


class BonusRequestBaseSerializer(ModelSerializer):
    status = SerializerMethodField()
    creator = SerializerMethodField()
    reviewer = SerializerMethodField()

    class Meta:
        model = BonusRequest
        fields = "__all__"
        read_only_fields = (
            "creator",
            "created_at",
            "updated_at",
            "price_usd",
            "payment_date",
        )

    def get_status(self, obj):
        return obj.status.status_name

    def get_creator(self, obj):
        return obj.creator.username

    def get_reviewer(self, obj):
        if not obj.reviewer:
            return None
        return obj.reviewer.username


class BonusRequestHistorySerializer(ModelSerializer):
    status = SerializerMethodField()

    class Meta:
        model = BonusRequestsHistory
        fields = (
            "status",
            "updated_at",
        )
        read_only_fields = (
            "status",
            "updated_at",
        )

    def get_status(self, obj):
        return obj.status.status_name


class FullHistorySerializer(ModelSerializer):
    history_requests = BonusRequestHistorySerializer(many=True, read_only=True)

    class Meta:
        model = BonusRequest
        fields = [
            "id",
            "creator",
            "reviewer",
            "bonus_type",
            "price_usd",
            "payment_date",
            "history_requests",
        ]


class BonusRequestStatusSerializer(ModelSerializer):
    class Meta:
        model = BonusRequestStatus
        fields = "__all__"


class BonusTypeSerializer(ModelSerializer):
    bonus_type = SerializerMethodField()

    class Meta:
        fields = ["bonus_type"]
        model = BonusRequest

    def get_bonus_type(self, obj):
        print(obj)
        return obj  # bonus type returns tuple for some reason
