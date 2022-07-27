from rest_framework.permissions import BasePermission


# from lannister_auth.models import LannisterUser


class IsUnregisteredMemberOfSlackWorkspace(BasePermission):
    def has_permission(self, request, view):
        if request.META.get("HTTP_X_SLACK_FRONTEND") == "slack-frontend-header":
            return True
        request_from_slack = request.META.get("HTTP_USER_AGENT")
        if request_from_slack and "Slackbot 1.0" in request_from_slack:
            return True

        return False


class IsMemberOfSlackWorkspace(BasePermission):
    message = "You're not a member of this Slack workspace, pls contact an admin"

    def has_permission(self, request, view):
        if request.META.get("HTTP_X_SLACK_FRONTEND") == "slack-frontend-header":
            return True
        request_from_slack = request.META.get("HTTP_USER_AGENT")
        if request_from_slack and "Slackbot 1.0" in request_from_slack:
            return True

        return False
