from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from lannister_slack.slack_client import slack_client
from lannister_slack.models import BonusRequest
from lannister_slack.serializers import BonusRequestSerializer
from lannister_slack.utils import prettify_json, BotMessage


@api_view(["POST"])
def respond_to_challenge(request):
    """View to respond to slack's request URL verification"""
    print(request.data)
    return Response(request.data["challenge"], status=status.HTTP_200_OK)


# grab bot's id so he won't trigger at his own messages later
BOT_ID = slack_client.api_call("auth.test")["user_id"]


class SlackEventView(APIView):
    """
    Main event view that handles all events that were enabled in app's dashboard

    Events are coming as POST requests
    """

    def post(self, request):
        """
        Echoes user's message written into bot's private messages or #slack-app channel
        """
        print(prettify_json(request.data))
        event = request.data["event"]
        if event["type"] == "message":
            if BOT_ID != event["user"]:
                slack_client.chat_postMessage(
                    channel=event["channel"], text=event["text"]
                )
        return Response(status=status.HTTP_200_OK)


class RegisterUserThroughSlackView(APIView):
    """
    Handler for '/register command'
    View is used for testing of slack commands api
    """

    def post(self, request):
        # print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        bot_message = BotMessage(channel, username)
        slack_client.chat_postMessage(**bot_message.register_response_markdown())
        return Response(status=status.HTTP_200_OK)


class ChooseActionView(APIView):
    """
    Handler for '/actions' command
    Should suggest using '/list-requests' or '/new-request' to the user
    Check 'user flow' slide for more
    https://docs.google.com/presentation/d/1EqXRMvbUFbwAnEkk7jZWgyDhzom56kYO32ZZvOv8_Vw/edit#slide=id.g135a3df236f_0_49
    """

    def post(self, request):
        print(prettify_json(request.data))
        # parse user_id, grab his permissions and move from there
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        bot_message = BotMessage(channel=channel, username=username)
        slack_client.chat_postMessage(**bot_message.actions_response_markdown())
        return Response(status=status.HTTP_200_OK)


class ListRequestsView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id", None)
        if not user_id:
            # raise some exception
            pass

        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        bonus_requests = BonusRequest.objects.filter(creator__slack_user_id=user_id)
        print(bonus_requests)
        bot_message = BotMessage(
            channel=channel, username=username, collection=bonus_requests
        )
        slack_client.chat_postMessage(**bot_message.list_requests_response_markdown())
        return Response(status=status.HTTP_200_OK)


class BonusRequestViewSet(ModelViewSet):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestSerializer
