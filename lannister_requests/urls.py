from django.urls import path, include
from lannister_requests.views import BonusRequestViewSet, HistoryRequestViewSet, BonusRequestStatusViewSet
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("", BonusRequestViewSet.as_view({'get': 'list', 'post': 'create'}), name="bonus-list"),
    path("<pk>", BonusRequestViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'}),
         name="bonus-single"),
    path("history/<pk>", HistoryRequestViewSet.as_view({'get': 'retrieve'}), name="history-single"),
    path("history/", HistoryRequestViewSet.as_view({'get': 'list'}), name="history-list"),
    path("status/", BonusRequestStatusViewSet.as_view({'get': 'list', 'post': 'create'}), name="status-list"),
    path("status/<pk>", BonusRequestStatusViewSet.as_view(
        {'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'}),
         name="status-single"),
]
