from django.urls import path
from lannister_slack.views import SlackEventView, BonusRequestViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("events", SlackEventView.as_view(), name="slack-events"),
]

router = DefaultRouter()
router.register("bonus-requests", BonusRequestViewSet)
urlpatterns += router.urls
