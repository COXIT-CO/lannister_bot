import os
from slack_sdk import WebClient

if os.environ.get("GITHUB_WORKFLOW"):
    bot_user_token = os.environ.get("BOT_USER_OAUTH_TOKEN")
    print("bot token:" + f"{bot_user_token}")
else:
    bot_user_token = os.getenv("BOT_USER_OAUTH_TOKEN")

slack_client = WebClient(token=bot_user_token)
