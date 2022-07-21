from rest_framework.viewsets import ModelViewSet
from lannister_roles.serializers import RoleSerializer
from lannister_roles.models import Role
from .permissions import IsAdministratorOrStaff
from rest_framework.permissions import IsAuthenticated


class RoleViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdministratorOrStaff,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer