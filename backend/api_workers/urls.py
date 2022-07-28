from django.urls import path
from .views import (
    ListWorkers,
    DetailWorker,
    ListWorkerRequest,
    DetailWorkerRequest,
)

urlpatterns = [
    # viewset-like url mapping,
    # 'workers/' should've been renamed in root to distinguish whether url is returning single object or collection
    path("list/", ListWorkers.as_view()),
    path("list/<str:reviewers>/", ListWorkers.as_view()),
    path("detail/<int:pk>/", DetailWorker.as_view(), name="worker-detail-id"),
    path(
        "detail/<str:username>/", DetailWorker.as_view(), name="worker-detail-username"
    ),
    path(
        "detail/<str:channel_id>",
        DetailWorker.as_view(),
        name="worker-detail-channel-id",
    ),
    path("request/", ListWorkerRequest.as_view()),
    path("request/<int:pk>/", DetailWorkerRequest.as_view()),
]
