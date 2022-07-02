from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from lannister_slack.slack_client import slack_client
from lannister_slack.models import BonusRequest
# from lannister_slack.serializers import BonusRequestSerializer
from lannister_slack.serializers import BonusRequestAdminSerializer, BonusRequestRewieverSerializer, BonusRequestBaseSerializer
from rest_framework.permissions import IsAuthenticated
from permissions import IsUser

import json


@api_view(["POST"])
def respond_to_challenge(request):
    """View to respond to slack's request URL verification"""
    print(request.data)
    return Response(request.data["challenge"], status=status.HTTP_200_OK)


def to_pretty_json(data):
    """
    Helper function that prettifies slack event data json

    Refactor to helpers/utils file later
    """
    return json.dumps(data, indent=4)


# grab bot's id so he won't trigger at his own messages later
BOT_ID = slack_client.api_call("auth.test")["user_id"]


class SlackEventView(APIView):
    """
    Main view that handles all events that were enabled in app's dashboard

    Events are coming as POST requests
    """

    def post(self, request):
        """
        Echoes user's message written into bot's private messages or #slack-app channel
        """
        print(to_pretty_json(request.data))
        event = request.data["event"]
        if event["type"] == "message":
            if BOT_ID != event["user"]:
                slack_client.chat_postMessage(
                    channel=event["channel"], text=event["text"]
                )
        return Response(status=status.HTTP_200_OK)


class BonusRequestViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsUser)
    queryset = BonusRequest.objects.all()

    # serializer_class = BonusRequestSerializer


    """
    TODO: Implement better get_serializer_class
    """
    methods = ["GET", "PATCH", "DELETE"]
    def get_serializer_class(self):
        if self.request.method in self.methods:
            if self.request.user.is_superuser:
                return BonusRequestAdminSerializer
            elif self.request.user.is_staff: #mock for refactoring after getting permissions
                return BonusRequestRewieverSerializer
        return BonusRequestBaseSerializer

    def get_queryset(self):
        """
        Another queryset for another groups
        NOW MOCK TILL HAVEN`T PERMISSIONS AND ROLE IMPLEMENT
        """
        queryset = self.queryset.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)




