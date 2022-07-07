from django.urls import path, include
"""When slack needed uncomment"""
# from lannister_slack.views import SlackEventView, BonusRequestViewSet
from rest_framework.routers import DefaultRouter


"""When slack needed uncomment"""
urlpatterns = [
#     path("events", SlackEventView.as_view(), name="slack-events"),
]

# router = DefaultRouter()
# router.register("bonus-requests", BonusRequestViewSet)
# urlpatterns += router.urls

