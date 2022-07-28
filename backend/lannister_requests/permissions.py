from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

"""
Skeleton for Roles implementing
"""


class IsUser(IsAuthenticated):
    def has_permission(self, request, view):
        # custom header is neccessary for the frontend to bypass jwt token verification of IsAuthenticated class, note: possible security breach
        if request.META.get("HTTP_X_SLACK_FRONTEND") == "slack-frontend-header":
            return True

        if not super().has_permission(request, view):
            return False

        if request.method in SAFE_METHODS:
            return True

        # return request.creator.username == request.user.username
