from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from lannister_auth.models import LannisterUser, Role
from lannister_requests.models import BonusRequest, BonusRequestStatus

# from lannister_slack.serializers import BonusRequestSerializer
from lannister_requests.serializers import (
    BonusRequestAdminSerializer,
    BonusRequestRewieverSerializer,
    BonusRequestBaseSerializer,
    FullHistorySerializer,
    BonusRequestStatusSerializer,
    BonusTypeSerializer,
)
from rest_framework.permissions import IsAuthenticated
from lannister_requests.permissions import IsUser
from rest_framework.response import Response
from rest_framework import status


class BonusRequestViewSet(ModelViewSet):
    permission_classes = (IsUser,)
    queryset = BonusRequest.objects.all()

    # serializer_class = BonusRequestSerializer

    """
    TODO: Implement better get_serializer_class
    """
    methods = ["GET", "PATCH", "DELETE"]

    def get_serializer_class(self):
        if self.request.method in self.methods:
            if self.request.user.is_superuser:
                return BonusRequestAdminSerializer
            elif (
                self.request.user.is_staff
            ):  # mock for refactoring after getting permissions
                return BonusRequestRewieverSerializer
        return BonusRequestBaseSerializer

    def get_queryset(self):
        """
        Handles query parameter like: /api/requests/?user=demigorrgon, to find bonus requests by user
        returns list if called on collection aka /api/requests/?user=demigorrgon
        returns single element on /api/requests/1?user=demigorrgon
        """
        if self.request.query_params.get("user"):
            queryset = self.queryset.filter(
                creator__username=self.request.query_params.get("user")
            )
            return queryset
        return self.queryset

    # def perform_create(self, serializer):
    #     serializer.save(creator=self.request.user)
    def create(self, request):
        # TODO: wrap in big try except clause
        data = request.data
        status_name = BonusRequestStatus.objects.get(status_name=data.get("status"))
        creator = LannisterUser.objects.get(username=data.get("creator"))
        reviewer = LannisterUser.objects.get(username=data.get("reviewer"))

        # TODO: think about caching Role.objects.get(id=2) in order to minimize db hits from queries
        if Role.objects.get(id=2) not in reviewer.roles.all():
            return Response(
                data={
                    "response": "Provided reviewer username is not a user with actual Reviewer role"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if creator == reviewer:
            return Response(
                data={"response": "You cannot assign yourself to review your ticket"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            float(data["price_usd"])
        except TypeError:
            return Response(
                data={"response": "Field 'price_usd' should be a decimal ie 123.00"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_bonus_request = BonusRequest.objects.create(
            status=status_name,
            creator=creator,
            reviewer=reviewer,
            description=data.get("description"),
            bonus_type=data.get("bonus_type").capitalize(),
            price_usd=data.get("price_usd"),
        )
        serializer = BonusRequestBaseSerializer(new_bonus_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HistoryRequestViewSet(ReadOnlyModelViewSet):

    """When get model of Roles implement permissions"""

    permission_classes = (IsAuthenticated,)
    serializer_class = FullHistorySerializer
    queryset = BonusRequest.objects.all()


class BonusRequestStatusViewSet(ModelViewSet):

    """When get model of Role implement permissions"""

    permission_classes = (IsAuthenticated,)
    serializer_class = BonusRequestStatusSerializer
    queryset = BonusRequestStatus.objects.all()


class BonusTypeView(ModelViewSet):
    queryset = BonusRequest.objects.values("bonus_type").distinct()
    serializer_class = BonusTypeSerializer
    http_method_names = ["get"]
