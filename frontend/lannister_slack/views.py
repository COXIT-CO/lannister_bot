import json
import re
from datetime import datetime
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from lannister_slack.slack_client import slack_client
from lannister_slack.utils import (
    prettify_json,
    BotMessage,
    ModalMessage,
    MessageWithDropdowns,
    # get_all_bonus_request_statuses,
    schedule_message_notification,
)
from lannister_slack.permissions import (
    IsMemberOfSlackWorkspace,
    IsUnregisteredMemberOfSlackWorkspace,
)

# from lannister_auth.models import LannisterUser, Role
from slack_sdk.errors import SlackApiError
from django.conf import settings


@api_view(["POST"])
def respond_to_challenge(request):
    """View to respond to slack's request URL verification, add it to urls.py when needed"""
    print(request.data)
    return Response(request.data["challenge"], status=status.HTTP_200_OK)


# grab bot's id so he won't trigger at his own messages later
BOT_ID = slack_client.api_call("auth.test")["user_id"]
# flag to check if user filled all required input fields (if there is multiple of them) before sending new command
HANGING_INPUT_FIELD = False
BASE_BACKEND_URL = settings.BASE_BACKEND_URL
FRONTEND_HEADER = settings.CUSTOM_FRONTEND_HEADER

"""
TODO: add HANGING_INPUT_FIELD check to all of the views, add /history handler
"""


def notify_user_about_hanging_field(channel, username=None):
    """
    Helper function to tell chat user that he didn't fill previous command/fields/forms/modals etc.
    """
    text = f"YOYOYOYOYO, {username}, chill, fill the fields from previous command\nData wasn't changed. Continue with new command or fill out missing stuff"
    # slack_client.chat_postMessage(channel=channel, text=text)
    bot_message = BotMessage(channel, username)
    slack_client.chat_postMessage(**bot_message.base_styled_message(f"{text}"))
    return Response(status=status.HTTP_403_FORBIDDEN)


class SlackEventView(APIView):
    """
    Main event View that handles all events that were enabled in app's dashboard

    Events are coming as POST requests
    """

    def post(self, request):
        """
        Returns help on users input (no slash commands)
        NOTE: apparently u can't output more than 10 blocks in one message, so there are 3 instances of bot messages I guess
        """
        print(f"Event: {prettify_json(request.data)}")
        event = request.data["event"]
        channel_id = event.get("channel")
        # user_id = event.get("user_id")
        # text = event.get("text")

        # requesting_user_username = requesting_user.json().get("username", None)
        if event["type"] == "message":
            if BOT_ID != event.get("user"):
                requesting_user = requests.get(
                    f"{settings.BASE_BACKEND_URL}workers/{channel_id}/"
                )

                if event.get("text") in ["help", "Help", "HELP", "hELP"]:
                    if requesting_user.status_code == 404:
                        error_msg = BotMessage(
                            channel_id, requesting_user.json().get("username")
                        )
                        slack_client.chat_postMessage(
                            **error_msg.base_styled_message("Pls run /register first")
                        )
                        return Response(
                            status=status.HTTP_200_OK, headers={"X-Slack-No-Retry": 1}
                        )  # has to return 200 cuz https://api.slack.com/apis/connections/events-api#the-events-api__responding-to-events
                    else:
                        first_part_bot_message = BotMessage(
                            channel=channel_id, username=requesting_user.get("username")
                        )
                        # scuffed pagination thanks to slack's limit of 10 messages
                        slack_client.chat_postMessage(
                            **first_part_bot_message.help_message_first_five()
                        )
                        second_part_bot_message = BotMessage(
                            channel=channel_id, username=requesting_user.get("username")
                        )
                        slack_client.chat_postMessage(
                            **second_part_bot_message.next_five_messages()
                        )
                        bot_message = BotMessage(
                            channel=channel_id, username=requesting_user.get("username")
                        )
                        slack_client.chat_postMessage(
                            **bot_message.base_styled_message(
                                f"*/list-users* - shows all users ADMIN ONLY\nYour channel id: {channel_id}\nYour slack username: {requesting_user.get('username')}"
                            )
                        )
                        return Response(
                            status=status.HTTP_200_OK, headers={"X-Slack-No-Retry": 1}
                        )
                # slack_client.chat_postMessage(channel=channel_id, text=text)

        return Response(status=status.HTTP_200_OK, headers={"X-Slack-No-Retry": 1})


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

        #         # trigger_id = loads.get("trigger_id")
        #         # modal_action_id = loads.get("view").get("blocks")
        if event_type == "view_submission":

            """
            Modal events are happening here
            """

            """
                Following code parses and processes automatically generated 'block_id' and 'action_id' by slack
                if you didn't provide 'block_id' and 'action_id' explicitly, slack shouldn't render your modal and should raise SlackApiError or some similar exception
                Might be helpful if you have dozen of input fields.
            """
            acquired_from_modal_messages = list(
                loads.get("view").get("state").get("values").values()
            )
            if (
                list(acquired_from_modal_messages[0].keys())[0]
                == "new_bonus_request_modal_type"
            ):
                channel_id = loads.get("view").get("blocks")[0].get("block_id")
                bot_message = BotMessage(channel=channel_id, username=username)
                selected_bonus_type = acquired_from_modal_messages[0][
                    "new_bonus_request_modal_type"
                ]["selected_option"]["text"]["text"]
                provided_description = acquired_from_modal_messages[1][
                    "new_bonus_request_modal_description"
                ]["value"]
                provided_reviewer = acquired_from_modal_messages[2][
                    "new_bonus_request_selected_reviewer"
                ]["selected_option"]["text"]["text"]
                provided_amount = acquired_from_modal_messages[3]["usd_amount"]["value"]
                provided_pay_date_str = acquired_from_modal_messages[4][
                    "datepicker-action"
                ]["selected_date"]
                provided_pay_time_str = acquired_from_modal_messages[5][
                    "new_bonus_request_selected_time"
                ]["selected_time"]

                provided_datetime = datetime.combine(
                    datetime.strptime(provided_pay_date_str, "%Y-%m-%d"),
                    datetime.strptime(provided_pay_time_str, "%H:%M").time(),
                )
                try:
                    provided_amount = float(provided_amount)
                except ValueError:
                    slack_client.chat_postMessage(
                        **bot_message.base_styled_message(
                            "*Amount should be a decimal ie: 123.00, 123, 321*"
                        )
                    )
                    return Response(status=status.HTTP_200_OK)

                new_bonus_request = requests.post(
                    url=settings.BASE_BACKEND_URL + "requests/",
                    json={
                        "status": "Created",
                        "creator": username,
                        "reviewer": provided_reviewer,
                        "description": provided_description,
                        "price_usd": provided_amount,
                        "bonus_type": selected_bonus_type,
                        "payment_date": f"{provided_pay_date_str} {provided_pay_time_str}",
                    },
                    headers=settings.CUSTOM_FRONTEND_HEADER,
                )
                find_reviewer_to_notify = requests.get(
                    url=f"{BASE_BACKEND_URL}workers/detail/{provided_reviewer}",
                    headers=FRONTEND_HEADER,
                ).json()
                reviewer_channel_id = find_reviewer_to_notify["slack_channel_id"]
                try:
                    schedule_message_notification(
                        channel=reviewer_channel_id,
                        username=username,
                        collection=new_bonus_request,
                        timestamp=provided_datetime.strftime("%d-%m-%Y %H:%M")
                        + " EEST",
                    )

                    slack_client.chat_postMessage(
                        **bot_message.base_styled_message(
                            "*Bonus request was registered successfully*"
                        )
                    )
                    bot_notification_to_reviewer = BotMessage(
                        channel=reviewer_channel_id,
                        username=username,
                        collection=new_bonus_request,
                    )  # NOTE: username param here is the username of the user filling out new bonus request to show his name to reviewer.
                    slack_client.chat_postMessage(
                        **bot_notification_to_reviewer.notification_for_reviewer()
                    )
                    return Response(status=status.HTTP_200_OK)
                except SlackApiError as e:
                    print(e)
                    slack_client.chat_postMessage(
                        **bot_message.base_styled_message(
                            "*Did you select a correct date and time?*\n*I cannot notify a reviewer in the past*\n"
                        )
                    )
                    return Response(
                        status=status.HTTP_200_OK
                    )  # slack doesn't close modals on 40x errors

            if (
                list(acquired_from_modal_messages[0].keys())[0]
                == "edit_request_bonus_type_selected"
            ):
                # get id from the title
                request_id = loads.get("view").get("title").get("text").split("#")[-1]
                # print(request_id)
                values = loads.get("view").get("state").get("values")
                bonus_type = (
                    values.get("edit_request_bonus_type_selected")
                    .get("edit_request_bonus_type_selected")
                    .get("selected_option")
                    .get("text")
                    .get("text")
                )
                description = (
                    values.get("edit_request_description_from_modal")
                    .get("edit_request_description_from_modal")
                    .get("value")
                )
                channel_id = (
                    loads.get("view").get("blocks")[0].get("block_id")
                )  # see comment in utils.py modal_on_bonus_request_edit() method
                bot_message = BotMessage(channel=channel_id, username=username)
                bonus_request_current_status = requests.get(
                    url=BASE_BACKEND_URL + "requests/" + request_id,
                    headers=FRONTEND_HEADER,
                ).json()["status"]

                if bonus_request_current_status != "Created":
                    slack_client.chat_postMessage(
                        **bot_message.base_styled_message(
                            "*This ticket was already reviewed.*\n*Consider adding a new ticket*"
                        )
                    )
                    return Response(
                        status=status.HTTP_200_OK
                    )  # have to return 200 or modal won't close and user will sit with WTF on his face

                patch_bonus_request = requests.patch(
                    url=BASE_BACKEND_URL + "requests/" + request_id,
                    json={"bonus_type": bonus_type, "description": description},
                    headers=FRONTEND_HEADER,
                )

                if patch_bonus_request.status_code == 200:
                    try:
                        schedule_message_notification(
                            channel=channel_id,
                            username=username,
                            collection=patch_bonus_request,
                            timestamp=patch_bonus_request.json()["payment_date"],
                        )
                        slack_client.chat_postMessage(
                            **bot_message.base_styled_message(
                                "*Bonus request updated successfully*"
                            )
                        )
                    except SlackApiError as e:
                        print(e)
                        slack_client.chat_postMessage(
                            **bot_message.base_styled_message(
                                "*Payment date of this request was expired*\n*Submit new ticket if you want*"
                            )
                        )
                    return Response(status=status.HTTP_200_OK)

                return Response(
                    data={
                        "response": "There was an error during editing request, is backend server running?"
                    }
                )

        #             # find all the fields that were sent from modal element
        #             message_values = [item.values() for item in acquired_from_modal_messages]
        #             messages_from_modal = [item[0].get("value") for item in message_values]
        #             print(messages_from_modal)

        #             # do something with acquired messages, might want to implement other checks before doing business logic
        #             return Response(status=status.HTTP_200_OK)

        if event_type == "block_actions":
            """
            Handles user's choices from dropdowns/actions with clicking buttons etc.
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
                    bot_message = BotMessage(channel=channel_id, username=username)

                    if request_from_dropdown.get("select_request").get(
                        "selected_option"
                    ) and reviewer_from_dropdown.get("select_reviewer").get(
                        "selected_option"
                    ):
                        HANGING_INPUT_FIELD = False
                        request_id = re.findall(
                            r"\s[0-9]+\s",
                            request_from_dropdown.get("select_request")
                            .get("selected_option")
                            .get("text")
                            .get("text"),
                        )[0].strip()

                        selected_reviewer_username = (
                            reviewer_from_dropdown.get("select_reviewer")
                            .get("selected_option")
                            .get("text")
                            .get("text")
                        )

                        bonus_request_to_patch_reviewer = requests.patch(
                            url=BASE_BACKEND_URL + f"requests/{request_id}",
                            json={"reviewer": selected_reviewer_username},
                            headers=FRONTEND_HEADER,
                        )
                        if bonus_request_to_patch_reviewer.status_code == 200:
                            slack_client.chat_postMessage(
                                **bot_message.base_styled_message(
                                    "*Reviewer assigned successfully.*\n"
                                )
                            )
                        else:
                            slack_client.chat_postMessage(
                                **bot_message.base_styled_message(
                                    "*You cannot assign bonus request review to yourself.*\n"
                                )
                            )
                            return Response(status=status.HTTP_200_OK)

                        get_reviewers_channel_id = requests.get(
                            url=BASE_BACKEND_URL
                            + f"workers/detail/{selected_reviewer_username}",
                            headers=FRONTEND_HEADER,
                        ).json()
                        message_reviewer = BotMessage(
                            channel=get_reviewers_channel_id.get("slack_channel_id"),
                            username=get_reviewers_channel_id.get("username"),
                            collection=bonus_request_to_patch_reviewer,
                        )
                        slack_client.chat_postMessage(
                            **message_reviewer.notification_for_reviewer()
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
                            **bot_message.base_styled_message(
                                "Fill out next option to proceed"
                            )
                        )
                        return Response(status=status.HTTP_200_OK)

                    else:
                        HANGING_INPUT_FIELD = True
                        return Response(status=status.HTTP_200_OK)

            if action_id == "edit_request":
                selected_request = (
                    loads.get("actions")[0]
                    .get("selected_option")
                    .get("text")
                    .get("text")
                )
                # parse string for bonus request id, change the way of parsing id when output in dropdown element is changed
                find_request_id = selected_request.split(": ")[1].split(" ")[0]
                print(find_request_id)
                # bonus_request_from_dropdown = BonusRequest.objects.get(
                #     id=int(find_request_id)
                # )
                selected_bonus_request = requests.get(
                    url=BASE_BACKEND_URL + "requests/" + find_request_id,
                    headers=FRONTEND_HEADER,
                )
                if selected_bonus_request.status_code == 404:
                    raise Exception(
                        "Bonus request selected by user in Slack was not found. Pls check find_request_id if you previously changed dropdown text output"
                    )
                print(selected_bonus_request)
                modal = ModalMessage(channel_id, username)
                slack_client.views_open(
                    trigger_id=loads.get("trigger_id"),
                    view=modal.modal_on_bonus_request_edit(request_id=find_request_id),
                    channel_id=channel_id,
                )
                return Response(status=status.HTTP_200_OK)

            if (
                action_id == "select_user_to_remove_from_reviewers"
                or action_id == "confirm_unassign"
            ):
                # protecting data from being used when interactive event fires up and only being selected in dropdown but button wasn't clicked
                if action_id == "confirm_unassign":
                    find_selected_username_to_unassign = (
                        loads.get("state").get("values").values()
                    )
                    selected_username_to_unassign = (
                        list(find_selected_username_to_unassign)[0]
                        .get("select_user_to_remove_from_reviewers")
                        .get("selected_option")["text"]["text"]
                        .split(" ")[1][:-1]
                    )
                    patch_users_role = requests.patch(
                        url=BASE_BACKEND_URL
                        + f"workers/detail/{selected_username_to_unassign}/",
                        json={"role": 2},
                        headers=FRONTEND_HEADER,
                    )
                    if patch_users_role.status_code == 200:
                        bot_message = BotMessage(channel=channel_id, username=username)
                        slack_client.chat_postMessage(
                            **bot_message.base_styled_message(
                                message="*Reviewer was removed successfully*"
                            )
                        )
                        return Response(status=status.HTTP_200_OK)
                    else:
                        bot_message = BotMessage(channel=channel_id, username=username)
                        slack_client.chat_postMessage(
                            **bot_message.base_styled_message(
                                message="*This user is not a reviewer.*\n*Perhaps you deleted him and forgot to /remove-reviewer?*"
                            )
                        )
                        return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_200_OK)

            if action_id == "update_request_from_list":
                bot_message = BotMessage(channel_id, username)
                slack_client.chat_postMessage(
                    **bot_message.base_styled_message(
                        "*Use /edit-request to edit your bonus request*"
                    )
                )
                return Response(status=status.HTTP_200_OK)

            if action_id == "confirm_register":
                user_data = requests.patch(
                    url=BASE_BACKEND_URL + "workers/" + username + "/",
                    json={"slack_user_id": loads.get("user").get("id")},
                )
                if user_data.status_code != 200:
                    raise Exception(
                        "Error when confirming register. Is backend server running at 8000 port?"
                    )
                bot_message = BotMessage(channel=channel_id, username=username)
                slack_client.chat_postMessage(
                    **bot_message.base_styled_message(
                        "*Thanks for registering in Lannister.*\n *Fill your first bonus request with /new-request*"
                    )
                )
                return Response(status=status.HTTP_200_OK)

        if action_id == "select_status_type" or action_id == "select_request_to_review":
            request_to_review = (
                loads.get("state").get("values").get("select_request_to_review")
            )
            status_type_selected = (
                loads.get("state").get("values").get("select_status_type")
            )
            if request_to_review.get("select_request_to_review").get(
                "selected_option"
            ).get("text").get("text") and status_type_selected.get(
                "select_status_type"
            ).get(
                "selected_option"
            ):
                HANGING_INPUT_FIELD = False
                selected_request_id = (
                    (
                        request_to_review.get("select_request_to_review")
                        .get("selected_option")
                        .get("text")
                        .get("text")
                    )
                    .split(": ")[1]
                    .split(" ")[0]
                )
                selected_status_type = (
                    status_type_selected.get("select_status_type")
                    .get("selected_option")
                    .get("text")
                    .get("text")
                )
                update_provided_bonus_request_status = requests.patch(
                    url=BASE_BACKEND_URL + f"requests/{selected_request_id}",
                    json={"status": selected_status_type},
                    headers=FRONTEND_HEADER,
                )
                if update_provided_bonus_request_status.status_code == 200:
                    bot_message = BotMessage(channel=channel_id, username=username)
                    slack_client.chat_postMessage(
                        **bot_message.base_styled_message(
                            "*Status updated successfully*"
                        )
                    )
                    ticket_creator = update_provided_bonus_request_status.json()[
                        "creator"
                    ]
                    ticket_creator_data = requests.get(
                        url=BASE_BACKEND_URL + f"workers/detail/{ticket_creator}",
                        headers=FRONTEND_HEADER,
                    ).json()
                    ticket_creator_username = ticket_creator_data["username"]
                    message_worker = BotMessage(
                        channel=ticket_creator_data["slack_channel_id"],
                        username=ticket_creator_username,
                    )
                    slack_client.chat_postMessage(
                        **message_worker.base_styled_message(
                            f"*Hey, {ticket_creator_username}, your ticket was reviewed*"
                        )
                    )
                    return Response(status=status.HTTP_200_OK)
            else:
                HANGING_INPUT_FIELD = True
                return Response(status=status.HTTP_200_OK)

        if action_id.startswith("approve"):
            request_id = action_id.split("_")[-1]
            find_request_to_approve = requests.patch(
                BASE_BACKEND_URL + f"requests/{request_id}",
                json={"status": "Approved"},
                headers=FRONTEND_HEADER,
            )
            if find_request_to_approve.status_code == 200:
                bot_message = BotMessage(
                    channel=loads.get("channel").get("id"), username=username
                )
                slack_client.chat_postMessage(
                    **bot_message.base_styled_message(
                        "*Bonus request approved ✅ successfully*"
                    )
                )
                return Response(status=status.HTTP_200_OK)

            bot_message = BotMessage(
                channel=loads.get("channel").get("id"), username=username
            )
            slack_client.chat_postMessage(
                **bot_message.base_styled_message("*Bonus request not found 💀*")
            )
            return Response(status=status.HTTP_404_NOT_FOUND)

        if action_id.startswith("reject"):
            request_id = action_id.split("_")[-1]
            find_request_to_reject = requests.patch(
                BASE_BACKEND_URL + f"requests/{request_id}",
                json={"status": "Rejected"},
                headers=FRONTEND_HEADER,
            )
            bot_message = BotMessage(
                channel=loads.get("channel").get("id"), username=username
            )
            if find_request_to_reject.status_code == 200:

                slack_client.chat_postMessage(
                    **bot_message.base_styled_message(
                        "*Bonus request rejected ❌ successfully*"
                    )
                )
                return Response(status=status.HTTP_200_OK)

            bot_message = BotMessage(
                channel=loads.get("channel").get("id"), username=username
            )
            slack_client.chat_postMessage(
                **bot_message.base_styled_message("*Bonus request not found 💀*")
            )
            return Response(status=status.HTTP_404_NOT_FOUND)

        if action_id.startswith("history"):
            if len(loads.get("actions")[0]["selected_options"]) == 0:
                bot_message = BotMessage(channel_id, username)
                slack_client.chat_postMessage(
                    **bot_message.base_styled_message(
                        "*You haven't selected anything, try agane*\nDEBUG: this multiple fields thing is clunky af"
                    )
                )
            # in this case id is in the string near '#' symbol
            pattern = r"\s#[0-9]+\s"
            history_of_selected_requests = []
            for item in loads.get("actions")[0][
                "selected_options"
            ]:  # this input field on frontend supports selection of multiple bonus requests, so loop through them
                selected_request_id = re.findall(pattern, item["text"]["text"])[
                    0
                ].strip()[1:]
                # request = BonusRequest.objects.get(id=int(selected_request_id))
                history_of_selected_bonus_request = requests.get(
                    url=BASE_BACKEND_URL + f"requests/history/{selected_request_id}",
                    headers=FRONTEND_HEADER,
                ).json()
                history_of_selected_requests.append(history_of_selected_bonus_request)

            for element in history_of_selected_requests:
                bot_message = BotMessage(
                    channel=channel_id,
                    username=username,
                    collection=element,
                )
                slack_client.chat_postMessage(**bot_message.history_static_output())
            # pass key from history as collection to botmessage, bonusrequesthistory queryset as queryset param
            return Response(status=status.HTTP_200_OK)


class RegisterUserCommandView(APIView):
    """
    Handler for '/register command'
    View is used to test slack commands api
    """

    permission_classes = (IsUnregisteredMemberOfSlackWorkspace,)

    def post(self, request):
        # query db and check if user has slack id
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel_id = request.data.get("channel_id", None)
        # user = LannisterUser.objects.get(username=username)
        user_data = requests.get(
            settings.BASE_BACKEND_URL + f"workers/detail/{username}"
        ).json()
        bot_message = BotMessage(channel_id, username)
        if user_data.get("slack_user_id") and user_data.get("slack_channel_id"):
            slack_client.chat_postMessage(
                **bot_message.base_styled_message("*You've already been registered*")
            )
            return Response(
                status=status.HTTP_200_OK,
            )
        # kwargs basically returns {channel_id: <id>, username: <username>, bots_picture: <some_emoji>, blocks: [some_slack_styling_blocks] if provided}
        # instead of manually typing it out all the time
        else:
            update_slack_ids = requests.patch(
                url=f"{settings.BASE_BACKEND_URL}workers/{username}/",
                json={"slack_channel_id": channel_id, "slack_user_id": None},
            ).json()
            print(update_slack_ids)
            slack_client.chat_postMessage(**bot_message.register())
            return Response(
                status=status.HTTP_201_CREATED,
            )


class ChooseActionCommandView(APIView):
    """
    Handler for '/actions' command
    Should suggest using '/list-requests' or '/new-request' to the user
    Check 'user flow' slide for more
    https://docs.google.com/presentation/d/1EqXRMvbUFbwAnEkk7jZWgyDhzom56kYO32ZZvOv8_Vw/edit#slide=id.g135a3df236f_0_49
    """

    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        # parse user_id, grab his permissions and move from there
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        if request.user.is_superuser:
            bot_message = BotMessage(channel=channel, username=username)
            slack_client.chat_postMessage(**bot_message.list_actions_admin())
            return Response(
                status=status.HTTP_200_OK,
            )

        bot_message = BotMessage(channel=channel, username=username)
        slack_client.chat_postMessage(**bot_message.list_actions_non_admin())
        return Response(
            status=status.HTTP_200_OK,
        )


class ListRequestsCommandView(APIView):
    """
    Reviewer and admin only, change behaviour by permission

    render buttons 'change status' and 'deny' or something from slack blocks example, on button change render dropdown in modal
    """

    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(request.data)
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        bonus_requests = requests.get(
            url=settings.BASE_BACKEND_URL + f"requests/?user={username}",
            headers={"X-slack-frontend": "slack-frontend-header"},
        ).json()
        bot_message = BotMessage(
            channel=channel, username=username, collection=bonus_requests
        )
        slack_client.chat_postMessage(**bot_message.list_requests())
        return Response(status=status.HTTP_200_OK)


class NewRequestCommandView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        trigger_id = request.data.get("trigger_id", None)
        # text = request.data.get("text", None)
        modal_message = ModalMessage(channel, username)
        # modal_message.modal_on_new_bonus_request()
        slack_client.views_open(
            trigger_id=trigger_id,
            view=modal_message.modal_on_new_bonus_request(channel_id=channel),
        )
        return Response(status=status.HTTP_200_OK)


class EditRequestCommandView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)

        bonus_requests_of_current_user = requests.get(
            url=BASE_BACKEND_URL + "requests/?user=" + username, headers=FRONTEND_HEADER
        ).json()

        # text = request.data.get("text", None)

        if len(bonus_requests_of_current_user) == 0:
            bot_message = BotMessage(channel, username)
            slack_client.chat_postMessage(
                **bot_message.base_styled_message(
                    "You haven't created any bonus requests.\n *Hint: proceed with /new-request*"
                )
            )
            return Response(status=status.HTTP_200_OK)
        # # print(bonus_requests)
        message = MessageWithDropdowns(
            channel, username, collection=bonus_requests_of_current_user
        )
        slack_client.chat_postMessage(**message.show_bonus_requests_by_user())
        return Response(status=status.HTTP_200_OK)


class ReviewRequestCommandView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)
        user_data = requests.get(
            url=BASE_BACKEND_URL + f"workers/detail/{username}"
        ).json()
        is_reviewer = {"name": "Reviewer"} in user_data["roles"]
        if is_reviewer:
            message = MessageWithDropdowns(channel, username)
            try:
                slack_client.chat_postMessage(**message.review_request_dropdown())
                return Response(status=status.HTTP_200_OK)
            except SlackApiError:
                bot_message = BotMessage(channel=channel, username=username)
                slack_client.chat_postMessage(
                    **bot_message.base_styled_message("*No bonus requests to review*")
                )
                return Response(status=status.HTTP_200_OK)
        else:
            bot_message = BotMessage(channel, username)
            slack_client.chat_postMessage(
                **bot_message.base_styled_message(
                    "You're not eligible to access this command"
                )
            )
            return Response(status=status.HTTP_403_FORBIDDEN)


class AddReviewerCommandView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        username = request.data.get("user_name", None)
        channel = request.data.get("channel_id", None)

        # if HANGING_INPUT_FIELD:
        #     notify_user_about_hanging_field(channel=channel)
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        reviewers_list = MessageWithDropdowns(
            channel=channel,
            username=username,
        )
        slack_client.chat_postMessage(**reviewers_list.assign_reviewer())
        return Response(status=status.HTTP_200_OK)
        # if len(LannisterUser.objects.filter(roles__in=[2])) > 0:
        #     bonus_request = BonusRequest.objects.filter(creator__username=username)
        #     reviewers_list = MessageWithDropdowns(
        #         channel=channel,
        #         username=username,
        #         queryset=bonus_request,
        #     )
        #     slack_client.chat_postMessage(**reviewers_list.assign_reviewer())
        #     return Response(status=status.HTTP_200_OK)

        # bot_message = BotMessage(channel, username)
        # slack_client.chat_postMessage(
        #     **bot_message.base_styled_message("*No reviewers added to lannister yet*\n")
        # )
        # return Response(status=status.HTTP_200_OK)


class RemoveReviewerCommandView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        channel_id = request.data.get("channel_id")
        username = request.data.get("user_name")
        # TODO: refactor into helper function | same with roles
        get_current_user = requests.get(
            url=BASE_BACKEND_URL + f"workers/detail/{username}", headers=FRONTEND_HEADER
        ).json()
        if {"name": "Administrator"} in get_current_user.get("roles"):
            message = MessageWithDropdowns(channel=channel_id, username=username)
            slack_client.chat_postMessage(**message.remove_reviewer_role_from_user())
            return Response(status=status.HTTP_200_OK)

        message = BotMessage(channel_id, username)
        slack_client.chat_postMessage(**message.access_denied())
        return Response(status=status.HTTP_403_FORBIDDEN)
        # returns 200 cuz 403 will not execute bot's styled response, blame slack not me


class ListUsersCommandView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        channel_id = request.data.get("channel_id")
        username = request.data.get("user_name")

        get_current_user = requests.get(
            url=BASE_BACKEND_URL + f"workers/detail/{username}", headers=FRONTEND_HEADER
        ).json()
        message = BotMessage(channel=channel_id, username=username)
        if {"name": "Administrator"} in get_current_user.get("roles"):
            slack_client.chat_postMessage(**message.list_users())
            return Response(status=status.HTTP_200_OK)

        slack_client.chat_postMessage(**message.access_denied())
        return Response(status=status.HTTP_403_FORBIDDEN)


class BonusRequestHistoryView(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        print(prettify_json(request.data))
        channel_id = request.data.get("channel_id")
        username = request.data.get("user_name")
        admin_role = {"name": "Administrator"}
        current_user_role = requests.get(
            url=BASE_BACKEND_URL + f"workers/detail/{username}"
        ).json()
        print(current_user_role)
        if admin_role in current_user_role.get("roles"):
            bot_message = MessageWithDropdowns(channel=channel_id, username=username)
            slack_client.chat_postMessage(**bot_message.history_dropdown())
            return Response(status=status.HTTP_200_OK)

        bot_message = BotMessage(channel=channel_id, username=username)
        slack_client.chat_postMessage(**bot_message.access_denied())
        return Response(status=status.HTTP_403_FORBIDDEN)


class ListReviewableRequests(APIView):
    permission_classes = (IsMemberOfSlackWorkspace,)

    def post(self, request):
        channel_id = request.data.get("channel_id")
        username = request.data.get("user_name")
        reviewer = requests.get(
            url=BASE_BACKEND_URL + f"workers/detail/{username}", headers=FRONTEND_HEADER
        ).json()
        reviewer_data = {"name": "Reviewer"}
        if reviewer_data in reviewer.get("roles"):
            all_reviewable_bonus_requests = requests.get(
                url=BASE_BACKEND_URL + f"requests/?reviewer={username}&reviewable=true",
                headers=FRONTEND_HEADER,
            ).json()
            bot_message = BotMessage(
                channel=channel_id,
                username=username,
                collection=all_reviewable_bonus_requests,
            )
            slack_client.chat_postMessage(
                **bot_message.list_reviewable_requests_by_current_reviewer()
            )
            return Response(status=status.HTTP_200_OK)

        bot_message = BotMessage(channel=channel_id, username=username)
        slack_client.chat_postMessage(**bot_message.access_denied())
        return Response(status=status.HTTP_403_FORBIDDEN)
