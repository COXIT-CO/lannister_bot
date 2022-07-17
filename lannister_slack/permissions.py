from rest_framework.permissions import BasePermission


# from lannister_auth.models import LannisterUser


class IsUnregisteredMemberOfSlackWorkspace(BaseException):
    def has_permission(self, request, view):
        request_from_slack = request.META.get("HTTP_USER_AGENT")
        if request_from_slack and "Slackbot 1.0" in request_from_slack:
            return True

        if request.user.is_authenticated:  # user sent jwt token with request
            return True

        return False


class IsMemberOfSlackWorkspace(BasePermission):
    message = "You're not a member of this Slack workspace, pls contact an admin"

    def has_permission(self, request, view):
        request_from_slack = request.META.get("HTTP_USER_AGENT")
        if request_from_slack and "Slackbot 1.0" in request_from_slack:
            print("from slack")
            return True

        if request.user.is_authenticated:
            if request.user.slack_user_id:
                return True

        return False
