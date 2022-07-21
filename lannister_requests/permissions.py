from rest_framework import permissions
from lannister_auth.models import Role
from lannister_requests.models import BonusRequestStatus


class IsUserOrAdministrator(permissions.IsAuthenticated):
    allowed_methods = ["GET", "POST", "PUT", "PATCH"]
    #allow DELETE request only when status is "Created" or user is "Administrator"
    def has_object_permission(self, request, view, obj):
        if request.method in self.allowed_methods:
            return True
        return (obj.creator == request.user and obj.status == BonusRequestStatus.objects.get(status_name="Created")) or \
               Role.objects.get(name="Administrator") in request.user.roles.all()


class IsAdministrator(permissions.BasePermission):
    methods = ["POST", "PUT", "PATCH", "DELETE"]

    def has_permission(self, request, view):
        if request.method in self.methods:
            return request.user.is_staff or request.user.is_superuser or \
                   Role.objects.get(name="Administrator") in request.user.roles.all()
        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
