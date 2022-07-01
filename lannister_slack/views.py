import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from lannister_slack.slack_client import slack_client
from lannister_slack.models import BonusRequest
from lannister_slack.serializers import BonusRequestSerializer
from lannister_slack.utils import (
    prettify_json,
    BotMessage,
    ModalMessage,
    ShowUserListMessage,
)
from lannister_auth.models import LannisterUser, Role


@api_view(["POST"])
def respond_to_challenge(request):
    """View to respond to slack's request URL verification"""
    print(request.data)
    return Response(request.data["challenge"], status=status.HTTP_200_OK)


# grab bot's id so he won't trigger at his own messages later
BOT_ID = slack_client.api_call("auth.test")["user_id"]


class SlackEventView(APIView):
    """
    Main event View that handles all events that were enabled in app's dashboard

    Events are coming as POST requests
    """

    def post(self, request):
        """
        Echoes user's message written into bot's private messages or #slack-app channel
        """
        print(prettify_json(request.data))
        event = request.data["event"]
        channel_id = event.get("channel")
        user_id = event.get("user_id")
        text = event.get("text")

        if event["type"] == "message":
            if user_id and BOT_ID != event["user"]:
                slack_client.chat_postMessage(channel=channel_id, text=text)
        return Response(status=status.HTTP_200_OK)


class InteractivesHandler(APIView):
    """
    Current view handles all the interactive elements such as button/modal/sending inputs from modal.
    It's a pretty shitty design, but ask slack api devs, not me
    https://api.slack.com/apps/A03MMSE5XR8/interactive-messages
    """

    def post(self, request):
        loads = json.loads(request.data["payload"])
        print(json.dumps(loads, indent=4))
        trigger_id = loads.get("trigger_id")
        event_type = loads.get("type")
        # actions = loads.get("actions")
        if event_type == "view_submission":

            # guess what, there is no other way to parse user's input from modal
            state_values = loads.get("view").get("state").get("values").values()
            message_values = [list(item.values()) for item in state_values]
            messages = [item[0].get("value") for item in message_values]
            print(messages)

            # do something with acquired messages, might want to implement other checks here before doing business logic
            return Response(status=status.HTTP_200_OK)

        if event_type == "block_actions":
            # TODO: handle user's selection of static field aka reviewer's choice etc.

            # if actions["type"] == "static_select":
            #     selected_reviewer = actions["selected_option"]["text"]["text"]
            #     reviewer = BonusRequest.objects.get(
            #         reviewer__username=selected_reviewer
            #     )
            #     print(reviewer)

            channel = loads.get("channel").get("id")
            username = loads.get("channel").get("id")
            button_text = loads.get("actions")[0].get("text").get("text")

            # check buttons text and determine which modal to open
            # there are no other unique identifiers for that particular button, probably except timestamps, which is already questionable /shrug
            if button_text == "Update request":
                modal = ModalMessage(channel, username)
                slack_client.views_open(
                    trigger_id=trigger_id,
                    view=modal.modal_on_update_request_button_click(),
                )
            return Response(status=status.HTTP_200_OK)


"""
TODO: refactor views by making base view (CommandView or smtng) which will store all the channel/user/text data and inherits from APIView or any other generic
"""


class RegisterUserCommandView(APIView):
    """
    Handler for '/register command'
    View is used for testing of slack commands api
    """

    def post(self, request):
        # query db and check if user has slack id, respond with denied if true, respond registered if false
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        bot_message = BotMessage(channel, username)
        slack_client.chat_postMessage(**bot_message.register_response_markdown())
        return Response(status=status.HTTP_200_OK)


class ChooseActionCommandView(APIView):
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


class ListRequestsCommandView(APIView):
    def post(self, request):
        print(request.data)
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


class NewRequestCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        # text = request.data.get("text", None)
        bot_message = BotMessage(channel, username)
        slack_client.chat_postMessage(**bot_message.new_request_response_markdown())
        return Response(status=status.HTTP_200_OK)


class EditRequestCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        text = request.data.get("text", None)
        # check permissions
        try:
            bonus_request = BonusRequest.objects.get(pk=text)
        except Exception as e:
            print(e)
            slack_client.chat_postMessage(
                channel=channel,
                text="Invalid bonus-request id. Hint: use /edit-request <request-id>",
            )
        print(bonus_request)
        bot_message = BotMessage(channel, username, collection=bonus_request)
        slack_client.chat_postMessage(**bot_message.edit_request_response_markdown())
        return Response(status=status.HTTP_200_OK)


class ReviewRequestCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        # username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        text = request.data.get("text", None)
        reviewer_role = Role.objects.get(id=2)
        reviewer = LannisterUser.objects.get(username=text)
        if reviewer_role in reviewer.roles.all():
            slack_client.chat_postMessage(
                channel=channel, text=f"Assigned *{reviewer}* successfully"
            )
        else:
            slack_client.chat_postMessage(
                channel=channel, text="Reviewer with such username does not exist"
            )

        return Response(status=status.HTTP_200_OK)


class AddReviewerCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        # text = request.data.get("text", None)
        bonus_request = BonusRequest.objects.filter(creator__username=username)
        print(bonus_request)
        reviewers = Role.objects.filter(users__in=[2]).first()
        reviewers_list = ShowUserListMessage(
            channel=channel,
            username=username,
            collection=reviewers,
            queryset=bonus_request,
        )

        slack_client.chat_postMessage(**reviewers_list.show_active_requests())
        return Response(status=status.HTTP_200_OK)


class BonusRequestViewSet(ModelViewSet):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestSerializer
