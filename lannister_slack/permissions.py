from rest_framework.permissions import BasePermission

# from lannister_auth.models import LannisterUser


class IsMemberOfSlackWorkspace(BasePermission):
    message = "You're not a member of this Slack workspace, pls contact an admin"

    def has_permission(self, request, view):
        request_from_slack = request.META.get("HTTP_USER_AGENT")
        if "Slackbot 1.0" in request_from_slack:
            print("from slack")
            return True

        try:
            if request.user.slack_user_id:
                return True
        except AttributeError:
            return False
        # return False
