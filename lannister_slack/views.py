import json
import re
from datetime import datetime
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
    MessageWithDropdowns,
)
from lannister_auth.models import LannisterUser, Role


@api_view(["POST"])
def respond_to_challenge(request):
    """View to respond to slack's request URL verification"""
    print(request.data)
    return Response(request.data["challenge"], status=status.HTTP_200_OK)


# grab bot's id so he won't trigger at his own messages later
BOT_ID = slack_client.api_call("auth.test")["user_id"]
# flag to check if user filled all required input fields (if there is multiple of them) before sending new command
HANGING_INPUT_FIELD = False


def notify_user_about_hanging_field(channel, username=None):
    """
    Helper function to tell chat user that he didn't fill previous command/fields/forms/modals etc.
    """
    text = f"YOYOYOYOYO, {username}, chill, fill the fields from previous command\nData wasn't changed. Continue with new command or fill out missing stuff"
    slack_client.chat_postMessage(channel=channel, text=text)
    return Response(status=status.HTTP_403_FORBIDDEN)


class SlackEventView(APIView):
    """
    Main event View that handles all events that were enabled in app's dashboard

    Events are coming as POST requests
    """

    def post(self, request):
        """
        Echoes user's message written into bot's private messages or #slack-app channel
        """
        # print(f"Event: {prettify_json(request.data)}")
        # event = request.data["event"]
        # channel_id = event.get("channel")
        # user_id = event.get("user_id")
        # text = event.get("text")
        # if event["type"] == "message":
        #     if BOT_ID != event["user"]:
        #         slack_client.chat_postMessage(channel=channel_id, text=text)
        return Response(status=status.HTTP_200_OK)


class InteractivesHandler(APIView):
    """
    Current view handles all the interactive elements such as user selecting stuff in dropdowns, button presses etc.
    It's a pretty shitty design, but ask slack api devs, not me
    https://api.slack.com/apps/A03MMSE5XR8/interactive-messages
    """

    def post(self, request):
        # request.data comes as {"payload": "somehugejsonstring"} so json.loads() it
        loads = json.loads(request.data["payload"])
        print(f"loads: {json.dumps(loads, indent=4)}")
        global HANGING_INPUT_FIELD
        username = loads.get("user").get("username")
        event_type = loads.get("type")

        trigger_id = loads.get("trigger_id")
        # modal_action_id = loads.get("view").get("blocks")
        if event_type == "view_submission":

            """
            Modal event is happening here
            """
            # TODO: refactor message format in utils, send state values explicitly in human-readable format

            """
                Following code parses and processes automatically generated 'block_id' and 'action_id' by slack
                if you didn't provide 'block_id' and 'action_id' explicitly
                Might be helpful if you have dozen of input fields.
            """

            aquired_from_modal_messages = list(
                loads.get("view").get("state").get("values").values()
            )
            print(prettify_json(aquired_from_modal_messages))
            if (
                list(aquired_from_modal_messages[0].keys())[0]
                == "new_bonus_request_modal_type"
            ):
                selected_bonus_type = aquired_from_modal_messages[0][
                    "new_bonus_request_modal_type"
                ]["selected_option"]["text"]["text"]
                provided_description = aquired_from_modal_messages[1][
                    "new_bonus_request_modal_description"
                ]["value"]
                provided_pay_date_str = aquired_from_modal_messages[2][
                    "datepicker-action"
                ]["selected_date"]
                provided_pay_date_datetime = datetime.strptime(
                    provided_pay_date_str, "%Y-%m-%d"
                )
                print(f"datetime: {provided_pay_date_datetime}")
                # bonus_type = BonusRequest.objects.filter(
                #     bonus_type=selected_bonus_type
                # ).exists()
                user = LannisterUser.objects.get(username=username)
                new_bonus_request = BonusRequest.objects.create(
                    creator=user,
                    bonus_type=selected_bonus_type,
                    description=provided_description,
                    payment_date=provided_pay_date_datetime,
                )
                new_bonus_request.save()
                # print("saved")
                # channel id is not available in interactions with modal idk why, TODO: find some workaround to send message to the user that something actually happened
                # response_msg = BotMessage(channel="D03MK2ADT29", username=username)
                # slack_client.chat_postMessage()
                return Response(status=status.HTTP_200_OK)

            # find all the fields that were sent from modal element
            message_values = [item.values() for item in aquired_from_modal_messages]
            messages_from_modal = [item[0].get("value") for item in message_values]
            print(messages_from_modal)

            # do something with acquired messages, might want to implement other checks here before doing business logic
            return Response(status=status.HTTP_200_OK)

        if event_type == "block_actions":
            """
            Handles user's choices from dropdowns
            """

            action_id = loads.get("actions")[0].get(
                "action_id"
            )  # not sure whether there could be more than 1 action at a time
            request_from_dropdown = (
                loads.get("state").get("values").get("bonus_request")
            )
            reviewer_from_dropdown = loads.get("state").get("values").get("reviewer")
            channel_id = loads.get("channel").get("id")

            if action_id == "select_request" or action_id == "select_reviewer":
                if request_from_dropdown and reviewer_from_dropdown:
                    if request_from_dropdown.get("select_request").get(
                        "selected_option"
                    ) and reviewer_from_dropdown.get("select_reviewer").get(
                        "selected_option"
                    ):
                        HANGING_INPUT_FIELD = False
                        slack_client.chat_postMessage(
                            channel=channel_id, text="Sent successfully"
                        )
                        return Response(status=status.HTTP_200_OK)

                    elif request_from_dropdown.get("select_request").get(
                        "selected_option"
                    ) or reviewer_from_dropdown.get("select_reviewer").get(
                        "selected_option"
                    ):
                        HANGING_INPUT_FIELD = True
                        # add styling from class
                        slack_client.chat_postMessage(
                            channel=channel_id, text="Select one more"
                        )
                        return Response(status=status.HTTP_200_OK)

                    else:
                        HANGING_INPUT_FIELD = True
                        return Response(status=status.HTTP_200_OK)

            if action_id == "edit_request":
                selected_request = (
                    loads.get("state")[0].get("selected_option").get("text").get("text")
                )
                # parse string for bonus request id, change the way of parsing id when output in dropdown element is changed
                find_request_id = re.findall(r"\s[0-9]\s", selected_request)[0].strip()
                print(find_request_id)
                bonus_request_from_dropdown = BonusRequest.objects.get(
                    id=int(find_request_id)
                )
                print(bonus_request_from_dropdown)
                # render modal

                modal = ModalMessage(channel_id, username)
                slack_client.views_open(
                    trigger_id=loads.get("trigger_id"),
                    view=modal.modal_on_bonus_request_edit(),
                )
                return Response(status=status.HTTP_200_OK)

            if (
                action_id == "select_user_to_remove_from_reviewers"
                or action_id == "confirm_unassign"
            ):
                print(action_id)
                # protecting data from being used when interactive event fires up and only being selected in dropdown but button wasn't clicked
                if action_id == "confirm_unassign":
                    # I have no idea what is a element in 'state': {"values": "somerandomshit"}, it's not documented so I had to find it this way
                    find_selected_username_to_unassign = (
                        loads.get("state").get("values").values()
                    )
                    selected_username_to_unassign = (
                        list(find_selected_username_to_unassign)[0]
                        .get("select_user_to_remove_from_reviewers")
                        .get("selected_option")["text"]["text"]
                        .split(" ")[1][:-1]
                    )
                    user_to_unassign = LannisterUser.objects.get(
                        username=selected_username_to_unassign
                    )
                    user_to_unassign.roles.remove(2)
                    user_to_unassign.save()
                    slack_client.chat_postMessage(
                        channel=channel_id, text="Unassigned successfully"
                    )
                    return Response(status=status.HTTP_200_OK)

            else:
                button_text = loads.get("actions")[0].get("text").get("text")
                # check buttons text and determine which modal to open
                # there are no other unique identifiers for that particular button, probably except timestamps, which is already questionable /shrug
                if button_text == "Update request":
                    modal = ModalMessage(channel_id, username)
                    slack_client.views_open(
                        trigger_id=trigger_id,
                        view=modal.modal_on_update_request_button_click(),
                    )
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_200_OK)


"""
TODO: refactor views by making base view (CommandView or smtng) which will store all the channel/user/text data and inherits from APIView or any other generic
"""


class RegisterUserCommandView(APIView):
    """
    Handler for '/register command'
    View is used to test slack commands api
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
    """
    Reviewer and admin only, change behaviour by permission

    TODO: should return history of status changes to admin
    render buttons 'change status' and 'deny' or something from slack blocks example, on button change render dropdown in modal
    """

    def post(self, request):
        print(request.data)
        user_id = request.data.get("user_id", None)
        # check permission

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
        trigger_id = request.data.get("trigger_id", None)
        # text = request.data.get("text", None)
        modal_message = ModalMessage(channel, username)
        # modal_message.modal_on_new_bonus_request()
        slack_client.views_open(
            trigger_id=trigger_id, view=modal_message.modal_on_new_bonus_request()
        )
        return Response(status=status.HTTP_200_OK)


class EditRequestCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        # text = request.data.get("text", None)
        current_user = LannisterUser.objects.get(username=username)
        bonus_requests = BonusRequest.objects.filter(creator=current_user)
        # print(bonus_requests)
        message = MessageWithDropdowns(channel, username, collection=bonus_requests)
        slack_client.chat_postMessage(**message.show_bonus_requests_by_user())
        return Response(status=status.HTTP_200_OK)


class ReviewRequestCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        reviewer_role = Role.objects.get(id=2)
        reviewer = LannisterUser.objects.get(username=username)
        if reviewer_role in reviewer.roles.all():
            # do the logic
            message = MessageWithDropdowns(channel, username)

            slack_client.chat_postMessage(**message.review_request_dropdown())
            slack_client.chat_postMessage(
                channel=channel,
                text="Modal should pop up here with the details. #TODO",
            )
            return Response(status=status.HTTP_200_OK)

        else:
            slack_client.chat_postMessage(
                channel=channel, text="You're not eligible to access this command"
            )
            return Response(status=status.HTTP_403_FORBIDDEN)


class AddReviewerCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)

        if HANGING_INPUT_FIELD is True:
            notify_user_about_hanging_field(channel=channel)
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            bonus_request = BonusRequest.objects.filter(creator__username=username)
            print(bonus_request)
            reviewers = Role.objects.filter(users__in=[2]).first()  # ???
            reviewers_list = MessageWithDropdowns(
                channel=channel,
                username=username,
                collection=reviewers,
                queryset=bonus_request,
            )

            slack_client.chat_postMessage(**reviewers_list.show_active_requests())
            return Response(status=status.HTTP_200_OK)


class RemoveReviewerCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        channel_id = request.data.get("channel_id")
        username = request.data.get("user_name")
        # TODO: refactor into helper function | same with roles
        requesting_user = LannisterUser.objects.get(username=username)
        is_admin = requesting_user.is_superuser
        if is_admin:
            # if is_requesting_user_admin:
            message = MessageWithDropdowns(channel=channel_id, username=username)
            slack_client.chat_postMessage(**message.remove_reviewer_role_from_user())
            return Response(status=status.HTTP_200_OK)

        message = BotMessage(channel_id, username)
        slack_client.chat_postMessage(**message.access_denied())
        return Response(status=status.HTTP_200_OK)


class ListUsersCommandView(APIView):
    def post(self, request):
        print(prettify_json(request.data))
        channel_id = request.data.get("channel_id")
        username = request.data.get("user_name")
        requesting_user = LannisterUser.objects.get(username=username)
        is_admin = requesting_user.is_superuser
        message = BotMessage(channel=channel_id, username=username)

        if is_admin:
            slack_client.chat_postMessage(**message.list_users())
            return Response(status=status.HTTP_200_OK)

        slack_client.chat_postMessage(**message.access_denied())
        return Response(status=status.HTTP_200_OK)


class BonusRequestViewSet(ModelViewSet):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestSerializer
