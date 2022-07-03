import json
import copy
from lannister_auth.models import LannisterUser
from lannister_slack.models import BonusRequest
from lannister_slack.serializers import BonusRequestSerializer
from lannister_auth.serializers import RoleSerializer, UserSerializer


def prettify_json(data):
    """
    Helper function that prettifies slack event data json

    Refactor to helpers/utils file later
    """
    return json.dumps(data, indent=4)


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
        # following variables are used only for passing querysets to them. Example: collection could be a queryset of all bonus requests of the user
        self.collection = collection
        self.queryset = queryset

        # construct markdown responses,
        # use mutability of dicts to construct text responses

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
            "value": None,
        }
        self.dropdown_in_modal = {
            "type": "input",
            "label": {
                "type": "plain_text",
                "text": None,
            },
            "element": {"type": "static_select", "options": []},
        }
        self.multiline_plain_text_input = {
            "type": "input",
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
                "initial_date": "2022-07-01",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True,
                },
                "action_id": "datepicker-action",
            },
            "label": {"type": "plain_text", "text": None, "emoji": True},
        }
        self.response = {
            # 'blocks' key should always return list of markdown elements such as header, body, buttons etc.
            "timestamp": self.timestamp,
            "channel": self.channel,
            "icon_emoji": self.icon_emoji,
            "blocks": [],
        }

        # TODO: refactor by adding assessory and options

    def register_response_markdown(self):
        self.header["text"]["text"] = f"*Hey, {self.username}, want to register?*"
        self.body["text"]["text"] = "*Type /credentials to continue*"
        self.response["blocks"] = [
            self.header,
            self.divider,
            self.body,
        ]
        return self.response

    def actions_response_markdown(self):
        self.body["text"]["text"] = "*Available commands: /new-request, /list-requests*"
        self.response["blocks"] = [self.divider, self.body, self.divider]
        return self.response

    def list_requests_response_markdown(self):
        self.header["text"]["text"] = "*List of requests*"
        serialized_collection = [
            BonusRequestSerializer(item).data for item in self.collection
        ]

        # create and construct string from Queryset passed as self.collection
        response_text = []
        for collection in serialized_collection:
            construct_text_response = f"*Request id: {collection['id']}*\n \
*Status: {collection['status']}*\n \
*Reviewer: {collection['reviewer']['username']}*\n \
- Request description: {collection['description']}\n \
- Request created at: {collection['created_at']}\n \
- Request last updated at: {collection['updated_at']}\n \
- Payment date: {collection['payment_date']}\n"
            response_text.append(construct_text_response)

        self.body["text"]["text"] = f"{''.join(item for item in response_text)}"
        self.button["block_id"] = "update_request_from_list"
        self.button["elements"][0]["action_id"] = "update_request_from_list"
        self.button["elements"][0]["text"]["text"] = "Update request"
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.divider,
            self.body,
            self.button,
        ]
        print(prettify_json(self.response))
        return self.response

    def new_request_response_markdown(self):
        self.header["text"]["text"] = "*Creating new bonus request, HUH?*"
        self.body["text"][
            "text"
        ] = "Pls send info in the following order divided by a comma: bonus-type, description, reviewer first and last name or his username"
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.divider,
            self.body,
            self.divider,
        ]
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

    # def edit_request_response_markdown(self):
    #     serialize_bonus_request = BonusRequestSerializer(self.collection).data
    #     self.body["text"]["text"] = f"*{prettify_json(serialize_bonus_request)}*"
    #     self.response["blocks"] = [self.divider, self.body, self.divider]
    #     return self.response


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

    def modal_on_bonus_request_edit(self):
        self.input["label"]["text"] = "Placeholder"
        self.response["title"]["text"] = "Edit bonus request"
        self.response["blocks"] = [
            self.divider,
            self.input,
            self.divider,
            self.input,
        ]
        print(prettify_json(self.response))
        return self.response

    def modal_on_new_bonus_request(self):
        self.response["title"]["text"] = "New bonus request"
        bonus_requests = BonusRequest.objects.all()
        bonus_types = set([item.bonus_type for item in bonus_requests])
        options = []
        for index, bonus_type in enumerate(bonus_types):
            option = copy.deepcopy(self.option)
            option["text"]["text"] = bonus_type
            option["value"] = f"value-{index}"
            options.append(option)
        self.dropdown_in_modal["label"]["text"] = "Select bonus type"
        self.dropdown_in_modal["element"]["options"] = options
        self.dropdown_in_modal["element"]["action_id"] = "new_bonus_request_modal_type"
        self.multiline_plain_text_input["element"][
            "action_id"
        ] = "new_bonus_request_modal_description"
        self.multiline_plain_text_input["label"]["text"] = "Add a description"
        self.datepicker["label"]["text"] = "Pick a payment date"
        self.response["blocks"] = [
            self.divider,
            self.dropdown_in_modal,
            self.multiline_plain_text_input,
            self.datepicker,
        ]
        # add reviewer input
        print(prettify_json(self.response))
        return self.response
        # bonus_type_field =


class MessageWithDropdowns(BotMessage):
    """
    Example: https://cutt.ly/LK0TNyW
    """

    def __init__(self, channel, username, collection=None, queryset=None):

        super().__init__(channel, username, collection, queryset)

    def show_active_requests(self):
        self.header["text"]["text"] = "Select from dropdowns"
        self.body["block_id"] = "bonus_request"
        self.body["text"]["text"] = "Select bonus request:"

        options = []
        serialized_requests = []
        for bonus_request in self.queryset:
            serialized_request = BonusRequestSerializer(bonus_request).data
            serialized_requests.append(serialized_request)

        for index, request in enumerate(serialized_requests):
            options.append(
                {
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": f"{request['bonus_type']} by: {request['creator']['username']} at {request['created_at']}",
                    },
                    "value": f"value-{index}",
                }
            )

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
        accessory_reviewers = {
            "type": "static_select",
            "action_id": "select_reviewer",
            "placeholder": {
                "type": "plain_text",
                "emoji": True,
                "text": "Enter reviewer's name",
            },
        }

        serialized_reviewers = RoleSerializer(self.collection).data
        options_reviewers = []
        for index, item in enumerate(serialized_reviewers.get("users")):
            options_reviewers.append(
                {
                    "text": {
                        "type": "plain_text",
                        "text": f"{item['username']}",
                    },
                    "value": f"value-{index}",
                }
            )

        accessory_reviewers["options"] = options_reviewers
        reviewers_part = {
            "type": "section",
            "block_id": "reviewer",
            "text": {"type": "mrkdwn", "text": "Select reviewer", "verbatim": False},
        }
        reviewers_part["accessory"] = accessory_reviewers
        return reviewers_part

    def show_bonus_requests_by_user(self):
        bonus_requests = []
        dropdown_choices = []
        for item in self.collection:
            serialized_bonus_request_by_user = BonusRequestSerializer(item).data
            bonus_requests.append(serialized_bonus_request_by_user)

        for index, bonus_request in enumerate(bonus_requests):
            option = {
                "text": {
                    "type": "plain_text",
                    "text": f"Request id: {bonus_request['id']} Created at: {bonus_request['created_at']}, status: {bonus_request['status']}",
                },
                "value": f"value-{index}",
            }
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
        reviewers_qs = LannisterUser.objects.filter(roles=2)
        reviewers = [UserSerializer(reviewer).data for reviewer in reviewers_qs]
        dropdown_choices = []
        for index, reviewer in enumerate(reviewers):
            option = {
                "text": {
                    "type": "plain_text",
                    "text": f"Reviewer: {reviewer['username']}, {reviewer['first_name']} {reviewer['last_name']}",
                },
                "value": f"value-{index}",
            }
            dropdown_choices.append(option)
        self.accessory["options"] = dropdown_choices
        self.response["blocks"] = [self.divider, self.body, self.button]
        print(prettify_json(self.response))
        return self.response

    def review_request_dropdown(self):
        self.header["text"]["text"] = "Review bonus request"
        self.body["text"]["text"] = "Select request to review"
        self.accessory["action_id"] = "select_request_to_review"
        not_reviewed_requests_qs = BonusRequest.objects.filter(status="Created")
        not_reviewed_requests = [
            BonusRequestSerializer(item).data for item in not_reviewed_requests_qs
        ]
        options = []
        for index, item in enumerate(not_reviewed_requests):
            option = copy.deepcopy(self.option)
            option["text"][
                "text"
            ] = f"{item['creator']['username']}'s request. Bonus type: {item['bonus_type']}"
            option["value"] = f"value-{index}"
            options.append(option)
        self.accessory["options"] = options
        self.body["accessory"] = self.accessory
        self.response["blocks"] = [self.header, self.divider, self.body]
        print(prettify_json(self.response))
        return self.response
