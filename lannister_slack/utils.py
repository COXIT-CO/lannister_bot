import json
from lannister_slack.serializers import BonusRequestSerializer


def prettify_json(data):
    """
    Helper function that prettifies slack event data json

    Refactor to helpers/utils file later
    """
    return json.dumps(data, indent=4)


# def convert_date_to_readable_eu_format(date):
#     return datetime.strptime(date, "%d-%m-%Y %H:%M")


class BotMessage:
    def __init__(self, channel, username, collection=None):
        """
        channel = channel_id from where slack's command was invoked
        username = username of a person who's pming the bot
        collections = expected QuerySet/list to style it up better
        """
        self.channel = channel
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.username = username
        self.collection = collection

        # construct markdown responses,
        # use mutability of dicts to construct text responses

        self.header = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": None,
            },
        }
        # header and body are the same in the structure (they're sections)
        # but split data into them for visibility
        self.body = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": None,
            },
        }

        # NOTE: buttons are interactive (using events) and
        # they're using Block kit https://api.slack.com/start/building/bolt-python#listening

        self.button = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": None},
                }
            ],
        }
        self.divider = {"type": "divider"}
        self.response = {
            # 'blocks' key should always return list of markdown element such as header, body, buttons etc.
            "ts": self.timestamp,
            "channel": self.channel,
            "icon_emoji": self.icon_emoji,
            "blocks": [],
        }

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
        self.button["elements"][0]["text"]["text"] = "Update request"
        self.response["blocks"] = [
            self.divider,
            self.header,
            self.divider,
            self.body,
            self.button,
        ]
        return self.response
