from django.urls import path

from .views import ListWorker
from .views import ListWorkerRequest, DetailWorkerRequest

urlpatterns = [
    path('', ListWorker.as_view()),
    path('<int:pk>/', DetailWorker.as_view()),
    path('request/', ListWorkerRequest.as_view()),
    path('request/<int:pk>/', DetailWorkerRequest.as_view()),
]