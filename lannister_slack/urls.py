from django.urls import path, include
from lannister_slack.views import SlackEventView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("events", SlackEventView.as_view(), name="slack-events"),
]
