from rest_framework.response import Response

from lannister_auth .models import LannisterUser
from rest_framework.viewsets import ModelViewSet
from .serializers import WorkerBaseSerializer, WorkerAdminSerializer
from lannister_roles.models import Role
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdministratorOrStaff


class WorkerViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdministratorOrStaff)
    queryset = LannisterUser.objects.all()

    def get_serializer_class(self):
        if Role.objects.get(name="Administrator") in self.request.user.roles.all() or self.request.user.is_superuser:
            return WorkerAdminSerializer
        return WorkerBaseSerializer

    def get_queryset(self):
        if Role.objects.get(name="Administrator") in self.request.user.roles.all() or self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(username=self.request.user.username)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        data = {}
        if self.request.data['roles'] != None:
            data['roles'] = self.request.data['roles'].split(',')
            serializer_data = self.get_serializer(instance, data=data, partial=partial)
            serializer_data.is_valid(raise_exception=True)
            self.perform_update(serializer_data)
            return Response(serializer_data.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

