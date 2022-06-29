from django.urls import path
from lannister_slack.views import SlackEventView


urlpatterns = [
    path("events", SlackEventView.as_view(), name="slack-events"),
]
