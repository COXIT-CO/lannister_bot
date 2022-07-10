import copy
import json
from datetime import datetime, timedelta
from lannister_auth.models import LannisterUser
from lannister_auth.serializers import UserSerializer
from lannister_slack.models import BonusRequest, BonusRequestStatus
from lannister_slack.serializers import (
    BonusRequestSerializer,
    BonusRequestStatusSerializer,
    BonusRequestHistory,
)
from .views import slack_client


def prettify_json(data):
    """
    Helper function that prettifies slack event data json

    Refactor to helpers/utils file later
    """
    return json.dumps(data, indent=4)


def list_requests_message_constructor(collection):
    return f"*Request id: {collection['id']}*\n \
*Status: {collection['status']['status_name']}*\n \
*Reviewer: {collection.get('reviewer').get('username') if collection.get('reviewer') else 'Unassigned'}*\n \
- Request description: {collection['description']}\n \
- Request created at: {collection['created_at']}\n \
- Request last updated at: {collection['updated_at']}\n \
- Payment date: {collection['payment_date']}\n"


def get_all_reviewers():
    reviewers_qs = LannisterUser.objects.filter(roles__in=[2])
    reviewers = [UserSerializer(reviewer).data for reviewer in reviewers_qs]
    return reviewers


def get_all_bonus_types():
    bonus_requests = BonusRequest.bonus_type.field.choices  # returns list of tuples
    bonus_types = set([choice[0] for choice in bonus_requests])
    return bonus_types


def get_all_bonus_request_statuses():
    status_choises = BonusRequestStatus.objects.all()
    statuses = [
        BonusRequestStatusSerializer(choice).data["status_name"]
        for choice in status_choises
    ]
    print(statuses)
    return statuses


def schedule_message_notification(channel, username, collection, timestamp):
    ts_to_epoch = timestamp.strftime("%s")
    bot_message = BotMessage(
        channel=channel, username=username, collection=collection, queryset=ts_to_epoch
    )
    slack_client.chat_scheduleMessage(**bot_message.notification_for_reviewer())
    return


# def convert_date_to_readable_eu_format(date):
#     return datetime.strptime(date, "%d-%m-%Y %H:%M")

# kinda anti SOLID for now
class BotMessage:
    def __init__(self, channel, username, collection=None, queryset=None):
        """
        channel = channel_id from where slack's command was invoked
        username = username of a person who's pming the bot
        collections = expected QuerySet/list to style it up better
        """
        self.channel = channel
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.username = username
        # TODO: rename variables for querysets from models, probably should've used *args tho
        # following variables are used only for passing querysets into them. Example: collection could be a queryset of all bonus requests of the user
        self.collection = collection
        self.queryset = queryset

        # construct markdown responses,
        # use mutability of dicts,
        # use copy.deepcopy if you need multiple unique elements from this constructor, shallow copy won't make desired element unique.
        # if you see the 'None' value, you're supposed to add something there or it will trigger SlackApiError. Made it that way specifically to simplify debugging of this shit.

        self.header = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": None,
            },
        }

        self.body = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": None,
            },
        }

        self.multiple_horizontal_text_elements = {"type": "section", "fields": []}
        self.markdown_text_from_multiple_horizontal_fields = {
            "type": "mrkdwn",
            "text": None,
        }
        # NOTE: buttons are interactive and
        # they're using Block kit https://api.slack.com/start/building/bolt-python#listening

        self.button = {
            "type": "actions",
            "block_id": None,
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": None},
                    "action_id": None,
                },
            ],
        }
        self.multiple_horizontal_buttons = {"type": "actions", "elements": []}
        self.singular_horizontal_button = {
            "type": "button",
            "text": {"type": "plain_text", "emoji": True, "text": None},
            "style": None,
            "value": None,
        }
        self.divider = {"type": "divider"}
        self.input = {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": None,
            },
            "element": {
                "type": "plain_text_input",
                "multiline": False,
                # "optional": True
                "action_id": "plain_text_input-action",
            },
        }
        self.accessory = {
            "type": "static_select",
            "action_id": "select_request",
            "placeholder": {
                "type": "plain_text",
                "text": "Choose request",
                "emoji": True,
            },
        }
        self.option = {
            "text": {
                "type": "plain_text",
                "text": None,
            },
            "value": None,  # should be unique if used in loop
        }
        self.dropdown_in_modal = {
            "type": "input",
            "block_id": None,
            "label": {
                "type": "plain_text",
                "text": None,
            },
            "element": {
                "type": "static_select",
                "options": [],
                "action_id": None,
            },
        }
        self.multiline_plain_text_input = {
            "type": "input",
            "block_id": None,
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "plain_text_input-action",
            },
            "label": {"type": "plain_text", "text": "Label", "emoji": True},
        }
        self.datepicker = {
            "type": "input",
            "element": {
                "type": "datepicker",
                "initial_date": "2022-07-01",  # only this date format is supported by slack
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True,
                },
                "action_id": "datepicker-action",
            },
            "label": {"type": "plain_text", "text": None, "emoji": True},
        }
        self.timepicker = {
            "type": "input",
            "element": {
                "type": "timepicker",
                "initial_time": "10:00",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select time",
                    "emoji": True,
                },
                "action_id": None,
            },
            "label": {
                "type": "plain_text",
                "text": None,
                "emoji": True,
            },
        }

        self.multi_static_select = {
            "type": "input",
            "element": {
                "type": "multi_static_select",
                "placeholder": {"type": "plain_text", "text": None, "emoji": True},
                "options": [],
                "action_id": None,
            },
            "label": {"type": "plain_text", "text": None, "emoji": True},
        }

        self.response = {
            # 'blocks' key should always return list of markdown elements such as divider, header, body, buttons etc.
            "timestamp": self.timestamp,
            "channel": self.channel,
            "icon_emoji": self.icon_emoji,
            "blocks": [],
        }

    def base_styled_message(self, message: str):
        """
        Basic bot's message with minimal styling,
        use it to show bot's emoji (avatar),
        add markdown styling to message passed to this method
        """
        self.body["text"]["text"] = message
        self.response["blocks"] = [self.divider, self.body, self.divider]
        return self.response

    def register(self):
        self.header["text"]["text"] = f"*Hey, {self.username}, want to register?*"
        self.body["text"][
            "text"
        ] = "Bot will automatically add your slack id to your Lannister account. Agreed?"
        self.button["block_id"] = "confirm_register"
        self.button["elements"][0]["text"]["text"] = "I agree"
        self.button["elements"][0]["action_id"] = "confirm_register"
        self.response["blocks"] = [self.header, self.divider, self.body, self.button]
        print(prettify_json(self.response))
        return self.response

    def list_actions_non_admin(self):
        self.body["text"]["text"] = "*Available commands: /list-users, /list-requests*"
        self.response["blocks"] = [self.divider, self.body, self.divider]
        return self.response

    def list_actions_admin(self):
        self.body["text"]["text"] = "*Available commands: /new-request, /list-requests*"
        self.response["blocks"] = [self.divider, self.body, self.divider]
        return self.response

    def list_requests(self):
        self.header["text"]["text"] = f"List of bonus requests by {self.username}"
        serialized_collection = [
            BonusRequestSerializer(item).data for item in self.collection
        ]
        print(serialized_collection)
        if len(serialized_collection) == 0:
            self.body["text"][
                "text"
            ] = "You haven't submitted any requests.\n*Hint*: /new-request"
            self.response["blocks"] = [self.header, self.divider, self.body]
            return self.response
        # create and construct string from Queryset passed as self.collection
        requests_list = []
        for collection in serialized_collection:
            construct_text_response = list_requests_message_constructor(collection)
            requests_list.append(construct_text_response)
        # print(requests_list)
        # self.body["text"]["text"] = f"{''.join(item for item in requests_list)}"
        self.button["block_id"] = "update_request_from_list"
        self.button["elements"][0]["action_id"] = "update_request_from_list"
        self.button["elements"][0]["text"]["text"] = "Update request"
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.divider,
        ]
        for request in requests_list:
            unique_request = copy.deepcopy(self.body)
            unique_request["text"]["text"] = request
            self.response["blocks"].append(unique_request)
            self.response["blocks"].append(self.divider)

        self.response["blocks"].append(self.button)
        print(prettify_json(self.response))
        return self.response

    def access_denied(self):
        # TODO: make this method reusable for different roles
        # TODO: add new account without admin privileges and test it out
        self.body["text"]["text"] = "You have to be an *admin* to use this command"
        self.response["blocks"] = [self.divider, self.body]
        return self.response

    def list_users(self):
        users = LannisterUser.objects.all()
        serialized_users = [UserSerializer(user).data for user in users]
        self.header["text"]["text"] = "List of users and their roles"
        self.response["blocks"] = [self.divider, self.header, self.divider]
        for user in serialized_users:
            users_data = copy.deepcopy(self.body)
            users_data["text"][
                "text"
            ] = f"User: {user.get('username')}, known as *{user.get('first_name')} {user.get('last_name')}*"
            self.response["blocks"].append(users_data)
        print(prettify_json(self.response))
        return self.response

    def notification_for_reviewer(self):
        self.header["text"]["text"] = "Hey, You! New bonus request to review"
        if self.queryset:  # check if timestamp for scheduled message exists
            self.response["post_at"] = self.queryset
            self.header["text"][
                "text"
            ] = "Deadline of this request is right now. Pls approve or reject:"
            self.response["text"] = "reviewer_notification"
        serialize_bonus_request = BonusRequestSerializer(self.collection)
        ticket_creator = self.body
        ticket_creator["text"][
            "text"
        ] = f'*{serialize_bonus_request.data.get("creator").get("username")} has requested the following stuff. Approve or reject it.*'
        ticket_status = copy.deepcopy(
            self.markdown_text_from_multiple_horizontal_fields
        )
        ticket_status[
            "text"
        ] = f'Current status: *{serialize_bonus_request.data.get("status").get("status_name")}*'
        bonus_type = copy.deepcopy(self.markdown_text_from_multiple_horizontal_fields)
        bonus_type[
            "text"
        ] = f'Bonus type: *{serialize_bonus_request.data.get("bonus_type")}*'
        requested_reward_in_usd = copy.deepcopy(
            self.markdown_text_from_multiple_horizontal_fields
        )
        requested_reward_in_usd[
            "text"
        ] = f'Requested reward amount: ${serialize_bonus_request.data.get("price_usd")}'
        description = copy.deepcopy(self.markdown_text_from_multiple_horizontal_fields)
        description[
            "text"
        ] = f'Description: *{serialize_bonus_request.data.get("description")}*'
        payment_date = copy.deepcopy(self.markdown_text_from_multiple_horizontal_fields)
        payment_date[
            "text"
        ] = f'Requested payment date: *{serialize_bonus_request.data.get("payment_date")}*'

        self.multiple_horizontal_text_elements["fields"] = [
            ticket_status,
            bonus_type,
            requested_reward_in_usd,
            description,
            payment_date,
        ]

        approve_button = copy.deepcopy(self.singular_horizontal_button)
        reject_button = copy.deepcopy(self.singular_horizontal_button)

        approve_button["text"]["text"] = "Approve"
        approve_button["action_id"] = f"approve_id_{self.collection.id}"
        approve_button["style"] = "primary"
        approve_button["value"] = "approved_request"
        self.multiple_horizontal_buttons["elements"].append(approve_button)
        reject_button["text"]["text"] = "Reject"
        reject_button["action_id"] = f"reject_id_{self.collection.id}"
        reject_button["style"] = "danger"
        reject_button["value"] = "rejected_request"
        self.multiple_horizontal_buttons["elements"].append(reject_button)
        self.response["blocks"] = [
            self.header,
            self.divider,
            self.body,
            self.divider,
            self.multiple_horizontal_text_elements,
            self.multiple_horizontal_buttons,
        ]

        print(prettify_json(self.response))
        return self.response

    def history_static_output(self):
        self.header["text"]["text"] = f"#{self.collection.id} request history"
        serialize_bonus_request = BonusRequestSerializer(self.collection)
        ticket_creator = copy.deepcopy(
            self.markdown_text_from_multiple_horizontal_fields
        )
        ticket_creator[
            "text"
        ] = f'By: {serialize_bonus_request.data.get("creator").get("username")}'
        bonus_type = copy.deepcopy(self.markdown_text_from_multiple_horizontal_fields)
        bonus_type[
            "text"
        ] = f'Bonus type: *{serialize_bonus_request.data.get("bonus_type")}*'
        requested_reward_in_usd = copy.deepcopy(
            self.markdown_text_from_multiple_horizontal_fields
        )
        requested_reward_in_usd[
            "text"
        ] = f'Requested reward amount: ${serialize_bonus_request.data.get("price_usd")}'
        description = copy.deepcopy(self.markdown_text_from_multiple_horizontal_fields)
        description[
            "text"
        ] = f'Description: *{serialize_bonus_request.data.get("description")}*'
        payment_date = copy.deepcopy(self.markdown_text_from_multiple_horizontal_fields)
        payment_date[
            "text"
        ] = f'Requested payment date: *{serialize_bonus_request.data.get("payment_date")}*'
        statuses = []
        serialized_history = [BonusRequestHistory(item).data for item in self.queryset]
        for item in serialized_history:  # grab status and updated_at
            print(item)
            history_display = f'Status: {item["status"]["status_name"]}, last updated at: {item["updated_at"]}'
            statuses.append(history_display)

        self.multiple_horizontal_text_elements["fields"] = [
            ticket_creator,
            bonus_type,
            requested_reward_in_usd,
            description,
            payment_date,
        ]
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.multiple_horizontal_text_elements,
        ]
        for item in statuses:
            status = copy.deepcopy(self.body)
            status["text"]["text"] = item
            self.response["blocks"].append(status)

        print(prettify_json(self.response))
        return self.response

    def list_reviewable_requests_by_current_reviewer(self):
        self.header["text"]["text"] = "Assigned bonus request tickets to me"
        serialized_tickets = [
            BonusRequestSerializer(item).data for item in self.collection
        ]
        print(serialized_tickets)
        self.response["blocks"] = [self.divider, self.header]
        for ticket in serialized_tickets:
            ticket_data = copy.deepcopy(self.body)
            ticket_data["text"][
                "text"
            ] = f"Ticket id: *#{ticket['id']}*\nSubmitted by: *{ticket['creator']['username']}*\nStatus: *{ticket['status']['status_name']}*\nPayment date: *{ticket['payment_date']}*\nDescription: *{ticket['description']}*\nLast time updated at: *{ticket['updated_at']}*"
            self.response["blocks"].append(ticket_data)

        print(prettify_json(self.response))
        return self.response


class ModalMessage(BotMessage):
    def __init__(self, channel, username, collection=None):
        super().__init__(channel, username, collection)
        self.response = {
            "type": "modal",
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "title": {
                "type": "plain_text",
                "text": None,  # your modal header text here
            },
        }
        self.option = {
            "text": {
                "type": "plain_text",
                "emoji": True,
                "text": None,
            },
            "value": None,
        }

    def modal_on_update_request_button_click(self):
        """
        Returns modal when "Update request" button was fired up
        Usecase: user types /list-requests, returns response with "Update request", user clicks "Update request" and this method should construct modal for this event
        """
        self.response["title"]["text"] = "Testing modal"

        self.input["label"]["text"] = "Type something"

        # example of manual block_id / action_id assignment idk if there is a reason to do so.
        first_input = copy.deepcopy(self.input)
        second_input = copy.deepcopy(self.input)
        first_input["block_id"] = "update_first_request_input"
        first_input["element"]["action_id"] = "update_first_request"
        second_input["block_id"] = "update_second_request_input"
        second_input["element"]["action_id"] = "update_second_request"

        self.response
        self.response["blocks"] = [
            self.divider,
            # self.input,
            first_input,
            self.divider,
            # self.input,
            second_input,
        ]
        print(f"modal: {prettify_json(self.response)}")
        return self.response

    def modal_on_bonus_request_edit(self, request_id=None):
        divider_with_channel_id = copy.deepcopy(
            self.divider
        )  # very dangerous workaround to find channel id in triggered modal, rework if possible
        divider_with_channel_id["block_id"] = self.channel
        bonus_types = get_all_bonus_types()
        self.dropdown_in_modal["label"]["text"] = "Edit bonus type"
        self.dropdown_in_modal["element"][
            "action_id"
        ] = "edit_request_bonus_type_selected"
        self.dropdown_in_modal["block_id"] = "edit_request_bonus_type_selected"

        options = []
        for index, bonus_type in enumerate(bonus_types):
            option = copy.deepcopy(self.option)
            option["text"]["text"] = bonus_type
            option["value"] = f"value-{index}"
            options.append(option)
        self.dropdown_in_modal["element"]["options"] = options
        self.multiline_plain_text_input[
            "block_id"
        ] = "edit_request_description_from_modal"
        self.multiline_plain_text_input["label"]["text"] = "Change description"
        self.multiline_plain_text_input["element"][
            "action_id"
        ] = "edit_request_description_from_modal"
        self.response["title"]["text"] = f"Edit bonus request #{request_id}"
        self.response["blocks"] = [
            divider_with_channel_id,
            self.dropdown_in_modal,
            self.divider,
            self.multiline_plain_text_input,
        ]
        print(prettify_json(self.response))
        return self.response

    def modal_on_new_bonus_request(self, channel_id):
        divider_with_channel_id = copy.deepcopy(self.divider)
        divider_with_channel_id["block_id"] = channel_id
        self.response["title"]["text"] = "New bonus request"
        reviewers_dropdown = copy.deepcopy(self.dropdown_in_modal)
        bonus_types = get_all_bonus_types()
        options = []
        for index, bonus_type in enumerate(bonus_types):
            option = copy.deepcopy(self.option)
            option["text"]["text"] = bonus_type
            option["value"] = f"value-{index}"
            options.append(option)
        bonus_type_dropdown = copy.deepcopy(self.dropdown_in_modal)
        bonus_type_dropdown["label"]["text"] = "Select bonus type"
        bonus_type_dropdown["block_id"] = "bonus_type_input"
        bonus_type_dropdown["element"]["options"] = options
        bonus_type_dropdown["element"]["action_id"] = "new_bonus_request_modal_type"
        self.multiline_plain_text_input["element"][
            "action_id"
        ] = "new_bonus_request_modal_description"
        self.multiline_plain_text_input["label"]["text"] = "Add a description"
        self.multiline_plain_text_input[
            "block_id"
        ] = "new_bonus_request_modal_description"
        self.datepicker["label"]["text"] = "Pick a payment date"
        self.datepicker["element"]["initial_date"] = datetime.today().strftime(
            "%Y-%m-%d"
        )

        self.timepicker["element"]["initial_time"] = (
            datetime.now() + timedelta(minutes=1)
        ).strftime("%H:%M")
        self.timepicker["element"]["placeholder"]["text"] = "Pick a payment time"
        self.timepicker["element"]["action_id"] = "new_bonus_request_selected_time"
        self.timepicker["label"]["text"] = "Pick a payment time"

        reviewers = get_all_reviewers()
        reviewers_dropdown["label"]["text"] = "Select a reviewer"
        reviewers_dropdown["element"][
            "action_id"
        ] = "new_bonus_request_selected_reviewer"
        reviewer_options = []
        for index, reviewer in enumerate(reviewers):
            option = copy.deepcopy(self.option)
            option["text"]["text"] = f"{reviewer.get('username')}"
            option["value"] = f"value-{index}"
            reviewer_options.append(option)
        reviewers_dropdown["block_id"] = "reviewers_dropdown_input"
        reviewers_dropdown["element"]["options"] = reviewer_options
        self.input["label"]["text"] = "Amount of reward you'd want in USD"
        self.input["block_id"] = "usd_amount"
        self.input["element"]["action_id"] = "usd_amount"
        self.response["blocks"] = [
            divider_with_channel_id,
            bonus_type_dropdown,
            self.multiline_plain_text_input,
            reviewers_dropdown,
            self.input,
            self.datepicker,
            self.timepicker,
        ]
        print(prettify_json(self.response))
        return self.response


class MessageWithDropdowns(BotMessage):
    """
    Example: https://cutt.ly/LK0TNyW
    """

    def __init__(self, channel, username, collection=None, queryset=None):

        super().__init__(channel, username, collection, queryset)

    def assign_reviewer(self):
        self.header["text"]["text"] = "Assign reviewer to your bonus request"
        self.body["block_id"] = "bonus_request"
        self.body["text"]["text"] = "Select bonus request:"

        options = []
        serialized_requests = []
        for bonus_request in self.queryset:
            serialized_request = BonusRequestSerializer(bonus_request).data
            serialized_requests.append(serialized_request)
        for index, request in enumerate(serialized_requests):
            option = copy.deepcopy(self.option)
            option["text"][
                "text"
            ] = f"id: {request['id']} {request['bonus_type']} by: {request['creator']['username']} at {request['created_at']}"
            option["value"] = f"value-{index}"
            options.append(option)

        self.accessory["options"] = options
        self.body["accessory"] = self.accessory
        self.response["channel"] = self.channel
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.divider,
            self.body,
            self.show_reviewers(),
        ]
        print(prettify_json(self.response))
        return self.response

    def show_reviewers(self):
        accessory_reviewers = copy.deepcopy(self.accessory)
        accessory_reviewers["action_id"] = "select_reviewer"
        accessory_reviewers["placeholder"]["text"] = "Enter reviewer's name"
        reviewers = get_all_reviewers()
        options_reviewers = []
        for index, item in enumerate(reviewers):
            option = copy.deepcopy(self.option)
            option["text"]["text"] = f"{item['username']}"
            option["value"] = f"value-{index}"
            options_reviewers.append(option)
        accessory_reviewers["options"] = options_reviewers
        reviewer_section = copy.deepcopy(self.body)
        reviewer_section["block_id"] = "reviewer"
        reviewer_section["text"]["text"] = "Select reviewer"
        reviewer_section["accessory"] = accessory_reviewers
        return reviewer_section

    def show_bonus_requests_by_user(self):
        bonus_requests = []
        dropdown_choices = []
        for item in self.collection:
            serialized_bonus_request_by_user = BonusRequestSerializer(item).data
            bonus_requests.append(serialized_bonus_request_by_user)

        for index, bonus_request in enumerate(bonus_requests):
            option = copy.deepcopy(self.option)
            option["text"][
                "text"
            ] = f"Request id: {bonus_request['id']} Created at: {bonus_request['created_at']}, status: {bonus_request['status']['status_name']}"
            option["value"] = f"value-{index}"
            dropdown_choices.append(option)
        self.header["text"]["text"] = "Select bonus request to edit"
        self.accessory["action_id"] = "edit_request"
        self.accessory["options"] = dropdown_choices
        self.body["text"]["text"] = "Pick one:"
        self.body["accessory"] = self.accessory
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.body,
        ]
        print(prettify_json(self.response))

        return self.response

    def remove_reviewer_role_from_user(self):
        self.accessory["action_id"] = "select_user_to_remove_from_reviewers"
        self.accessory["placeholder"]["text"] = "Select user to unassign."
        self.body["text"][
            "text"
        ] = "Pick reviewer to unassign.\n*Note: after user was removed, rerun the command*"
        self.body["accessory"] = self.accessory
        self.button["block_id"] = "confirm_unassign"
        self.button["elements"][0]["action_id"] = "confirm_unassign"
        self.button["elements"][0]["text"]["text"] = "Confirm unassign"
        reviewers = get_all_reviewers()
        dropdown_choices = []
        for index, reviewer in enumerate(reviewers):
            option = copy.deepcopy(self.option)
            option["text"][
                "text"
            ] = f"Reviewer: {reviewer['username']}, {reviewer['first_name']} {reviewer['last_name']}"
            option["value"] = f"value-{index}"
            dropdown_choices.append(option)
        self.accessory["options"] = dropdown_choices
        self.response["blocks"] = [self.divider, self.body, self.button]
        print(prettify_json(self.response))
        return self.response

    def review_request_dropdown(self):
        self.header["text"]["text"] = "Review bonus request"
        self.body["text"]["text"] = "Select request to review"
        requests_selection = copy.deepcopy(self.accessory)
        requests_selection["action_id"] = "select_request_to_review"
        not_reviewed_requests_qs = BonusRequest.objects.filter(
            status__status_name="Created"
        )
        not_reviewed_requests = [
            BonusRequestSerializer(item).data for item in not_reviewed_requests_qs
        ]
        options = []
        for index, item in enumerate(not_reviewed_requests):
            option = copy.deepcopy(self.option)
            option["text"][
                "text"
            ] = f"id: {item['id']} by {item['creator']['username']}. Bonus type: {item['bonus_type']}"
            option["value"] = f"value-{index}"
            options.append(option)
        requests_selection["options"] = options
        requests_selection_body = copy.deepcopy(self.body)
        requests_selection_body["accessory"] = requests_selection
        requests_selection_body["block_id"] = "select_request_to_review"
        bonus_type_statuses = get_all_bonus_request_statuses()
        bonus_type_statuses_to_select = copy.deepcopy(self.accessory)
        bonus_type_statuses_to_select["action_id"] = "select_status_type"
        bonus_type_statuses_to_select["placeholder"]["text"] = "Choose status type"
        bonus_type_options = []
        for index, status in enumerate(bonus_type_statuses):
            option = copy.deepcopy(self.option)
            option["text"]["text"] = status
            option["value"] = f"value-{index}"
            bonus_type_options.append(option)
        bonus_type_statuses_to_select["options"] = bonus_type_options
        bonus_type_selection_body = copy.deepcopy(self.body)
        bonus_type_selection_body["text"][
            "text"
        ] = "Pick a status for provided request:"
        bonus_type_selection_body["accessory"] = bonus_type_statuses_to_select
        bonus_type_selection_body["block_id"] = "select_status_type"
        self.response["blocks"] = [
            self.header,
            self.divider,
            requests_selection_body,
            self.divider,
            bonus_type_selection_body,
        ]
        print(prettify_json(self.response))
        return self.response

    def history_dropdown(self):
        self.header["text"]["text"] = "History of Bonus Requests"
        self.multi_static_select["element"]["placeholder"][
            "text"
        ] = "Click to see the list"
        self.multi_static_select["label"][
            "text"
        ] = "Select bonus request to see its history of statuses"
        bonus_requests = BonusRequest.objects.all()
        if len(bonus_requests) == 0:
            self.body["text"][
                "text"
            ] = "*No bonus requests were created.\n/new-request to add some*"
            self.response["blocks"] = [self.divider, self.body, self.divider]
            return self.response

        serialized_requests = [
            BonusRequestSerializer(item).data for item in bonus_requests
        ]
        options = []
        for index, request in enumerate(serialized_requests):
            option = copy.deepcopy(self.option)
            option["text"][
                "text"
            ] = f"{request['creator']['username']}'s {request['bonus_type']} request #{request['id']} for ${request['price_usd']}"
            option["value"] = f"value-{index}"
            options.append(option)

        self.multi_static_select["element"]["options"] = options
        self.multi_static_select["element"][
            "action_id"
        ] = "history_bonus_request_select"

        self.response["blocks"] = [
            self.divider,
            self.header,
            self.divider,
            self.multi_static_select,
        ]
        print(prettify_json(self.response))
        return self.response
