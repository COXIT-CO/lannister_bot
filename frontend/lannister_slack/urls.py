from django.urls import path
from lannister_slack.views import (
    SlackEventView,
    InteractivesHandler,
    RegisterUserCommandView,
    ChooseActionCommandView,
    ListRequestsCommandView,
    NewRequestCommandView,
    EditRequestCommandView,
    ReviewRequestCommandView,
    AddReviewerCommandView,
    RemoveReviewerCommandView,
    ListUsersCommandView,
    BonusRequestHistoryView,
    ListReviewableRequests,
    # respond_to_challenge,
)

urlpatterns = [
    # path("events", respond_to_challenge, name="slack-events"),
    path("events", SlackEventView.as_view(), name="slack-events"),
    path("interactives", InteractivesHandler.as_view(), name="interactives"),
    path("register", RegisterUserCommandView.as_view(), name="register-in-slack"),
    path("actions", ChooseActionCommandView.as_view(), name="choose-actions"),
    path("list-requests", ListRequestsCommandView.as_view(), name="list-requests"),
    path("new-request", NewRequestCommandView.as_view(), name="new-request"),
    path("edit-request", EditRequestCommandView.as_view(), name="edit-request"),
    path("review-request", ReviewRequestCommandView.as_view(), name="review-request"),
    path("add-reviewer", AddReviewerCommandView.as_view(), name="add-reviewer"),
    path(
        "remove-reviewer", RemoveReviewerCommandView.as_view(), name="remove-reviewer"
    ),
    path("history", BonusRequestHistoryView.as_view(), name="history"),
    path("list-users", ListUsersCommandView.as_view(), name="list-users"),
    path(
        "list-requests-to-review",
        ListReviewableRequests.as_view(),
        name="list-requests-to-review",
    ),
]
