from django.urls import path
from lannister_slack.views import (
    SlackEventView,
    BonusRequestViewSet,
    RegisterUserThroughSlackView,
    ChooseActionView,
    ListRequestsView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("events", SlackEventView.as_view(), name="slack-events"),
    path("register", RegisterUserThroughSlackView.as_view(), name="register-in-slack"),
    path("actions", ChooseActionView.as_view(), name="choose-actions"),
    path("list-requests", ListRequestsView.as_view(), name="list-requests"),
]

router = DefaultRouter()
router.register("bonus-requests", BonusRequestViewSet)
urlpatterns += router.urls
