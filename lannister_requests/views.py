from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from lannister_requests.models import BonusRequest, BonusRequestStatus
from lannister_requests.serializers import BonusRequestAdminSerializer, BonusRequestRewieverSerializer, \
    BonusRequestBaseSerializer, FullHistorySerializer, BonusRequestStatusSerializer
from rest_framework.permissions import IsAuthenticated
from lannister_requests.permissions import IsUserOrAdministrator, IsAdministrator, IsHistory
from lannister_auth.models import Role


class BonusRequestViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsUserOrAdministrator, )
    queryset = BonusRequest.objects.all().order_by('creator', 'reviewer')

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            if self.request.user.is_superuser or self.request.user.is_staff \
                    or Role.objects.get(name="Administrator") in self.request.user.roles.all():
                return BonusRequestAdminSerializer
            elif Role.objects.get(name="Reviewer") in self.request.user.roles.all():
                return BonusRequestRewieverSerializer
        return BonusRequestBaseSerializer

    def get_queryset(self):
        worker_queryset = Role.objects.none()
        reviewer_queryset = Role.objects.none()
        admin_queryset = Role.objects.none()
        if Role.objects.get(name="Worker") in self.request.user.roles.all():
            worker_queryset = self.queryset.filter(creator=self.request.user)
        if Role.objects.get(name="Reviewer") in self.request.user.roles.all():
            reviewer_queryset = self.queryset.filter(reviewer=self.request.user)
        if Role.objects.get(name="Administrator") in self.request.user.roles.all():
            admin_queryset = self.queryset.all().exclude(creator=self.request.user)
        result = worker_queryset | reviewer_queryset | admin_queryset
        return result

    def perform_update(self, serializer):
        if Role.objects.get(name="Administrator") not in self.request.user.roles.all() and \
                (serializer.validated_data.get('reviewer') or serializer.validated_data.get('description')) and\
                self.request.user != self.get_object().creator:
            res = serializers.ValidationError({'message' : 'You cannot update this field of not YOUR request'})
            res.status_code = 406
            raise res
        if Role.objects.get(name="Administrator") not in self.request.user.roles.all() and \
                (serializer.validated_data.get('status') or serializer.validated_data.get('price_usd') or
            serializer.validated_data.get('payment_date')) and self.request.user == self.get_object().creator:
            res = serializers.ValidationError({'message' : 'You cannot update this field of YOUR request'})
            res.status_code = 406
            raise res
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)



class HistoryRequestViewSet(ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticated, IsHistory)
    serializer_class = FullHistorySerializer
    queryset = BonusRequest.objects.all().order_by('creator', 'reviewer')

    def get_queryset(self):
        worker_queryset = Role.objects.none()
        reviewer_queryset = Role.objects.none()
        admin_queryset = Role.objects.none()
        if Role.objects.get(name="Worker") in self.request.user.roles.all():
            worker_queryset = self.queryset.filter(creator=self.request.user)
        if Role.objects.get(name="Reviewer") in self.request.user.roles.all():
            reviewer_queryset = self.queryset.filter(reviewer=self.request.user)
        if Role.objects.get(name="Administrator") in self.request.user.roles.all():
            admin_queryset = self.queryset.all().exclude(creator=self.request.user)
        result = worker_queryset | reviewer_queryset | admin_queryset
        return result

class BonusRequestStatusViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, IsAdministrator, )
    serializer_class = BonusRequestStatusSerializer
    queryset = BonusRequestStatus.objects.all()


