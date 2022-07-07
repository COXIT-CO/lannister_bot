from rest_framework.viewsets import ModelViewSet
from lannister_requests.models import BonusRequest
# from lannister_slack.serializers import BonusRequestSerializer
from lannister_requests.serializers import BonusRequestAdminSerializer, BonusRequestRewieverSerializer, \
    BonusRequestBaseSerializer, FullHistorySerializer
from rest_framework.permissions import IsAuthenticated
from lannister_requests.permissions import IsUser


class BonusRequestViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsUser, )
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
            elif self.request.user.is_staff: #mock for refactoring after getting permissions
                return BonusRequestRewieverSerializer
        return BonusRequestBaseSerializer

    def get_queryset(self):
        """
        Another queryset for each groups
        NOW MOCK TILL HAVEN`T PERMISSIONS AND ROLE IMPLEMENT
        """
        queryset = self.queryset.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



class HistoryRequestViewSet(ModelViewSet):

    """When get model of Roles implement permissions"""
    permission_classes = (IsAuthenticated,)
    serializer_class = FullHistorySerializer
    queryset = BonusRequest.objects.all()


