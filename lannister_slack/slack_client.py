import os
from slack_sdk import WebClient

bot_user_token = os.getenv("BOT_USER_OAUTH_TOKEN")

slack_client = WebClient(token=bot_user_token)
