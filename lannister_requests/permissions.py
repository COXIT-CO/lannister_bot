from rest_framework.permissions import BasePermission

"""
Skeleton for Roles implementing
"""
class IsUser(BasePermission):
    allowed_methods = ["GET", "POST", "PUT", "PATCH"]

    def has_object_permission(self, request, view, obj):
        if request.method in self.allowed_methods:
            return True
        return obj.username == request.user.username
