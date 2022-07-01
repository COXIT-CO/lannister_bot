from django.urls import path
from lannister_slack.views import (
    SlackEventView,
    InteractivesHandler,
    BonusRequestViewSet,
    RegisterUserCommandView,
    ChooseActionCommandView,
    ListRequestsCommandView,
    NewRequestCommandView,
    EditRequestCommandView,
    ReviewRequestCommandView,
    AddReviewerCommandView,
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("events", SlackEventView.as_view(), name="slack-events"),
    path("interactives", InteractivesHandler.as_view(), name="interactives"),
    path("register", RegisterUserCommandView.as_view(), name="register-in-slack"),
    path("actions", ChooseActionCommandView.as_view(), name="choose-actions"),
    path("list-requests", ListRequestsCommandView.as_view(), name="list-requests"),
    path("new-request", NewRequestCommandView.as_view(), name="new-requests"),
    path("edit-request", EditRequestCommandView.as_view(), name="edit-request"),
    path("review-request", ReviewRequestCommandView.as_view(), name="new-requests"),
    path("add-reviewer", AddReviewerCommandView.as_view(), name="new-requests"),
    # path("remove-reviewer", NewRequestCommandView.as_view(), name="new-requests"),
    # path("history", NewRequestCommandView.as_view(), name="new-requests"),
    # path("list-users", NewRequestCommandView.as_view(), name="new-requests"),
]

router = DefaultRouter()
router.register("bonus-requests", BonusRequestViewSet)
urlpatterns += router.urls
