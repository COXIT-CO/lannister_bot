from rest_framework.permissions import BasePermission
from lannister_roles.models import Role

class IsAdministratorOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.is_staff or request.user.is_superuser or \
                   Role.objects.get(name="Administrator") in request.user.roles.all()
        return True
