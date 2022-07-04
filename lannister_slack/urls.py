from django.urls import path, include
"""When slack needed uncomment"""
# from lannister_slack.views import SlackEventView, BonusRequestViewSet
from lannister_slack.views import BonusRequestViewSet, HistoryRequestViewSet
from rest_framework.routers import DefaultRouter


"""When slack needed uncomment"""
urlpatterns = [
#     path("events", SlackEventView.as_view(), name="slack-events"),
    path("requests/", BonusRequestViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("requests/<pk>", BonusRequestViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'})),
    path("requests/history/<pk>", HistoryRequestViewSet.as_view({'get': 'retrieve'})),
    path("requests/history/", HistoryRequestViewSet.as_view({'get': 'list'})),
]

# router = DefaultRouter()
# router.register("bonus-requests", BonusRequestViewSet)
# urlpatterns += router.urls

