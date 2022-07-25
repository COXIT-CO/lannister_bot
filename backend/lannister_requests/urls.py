from django.urls import path
from lannister_requests.views import (
    BonusRequestViewSet,
    BonusTypeView,
    HistoryRequestViewSet,
    BonusRequestStatusViewSet,
)


urlpatterns = [
    path("", BonusRequestViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "<pk>",
        BonusRequestViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
        ),
    ),
    path("history/<pk>", HistoryRequestViewSet.as_view({"get": "retrieve"})),
    path("history/", HistoryRequestViewSet.as_view({"get": "list"})),
    path(
        "status/", BonusRequestStatusViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        "status/<pk>",
        BonusRequestStatusViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
        ),
    ),
    path("bonus-types/", BonusTypeView.as_view({"get": "list"})),
]
