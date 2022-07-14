from django.urls import path

from .views import ListWorker, DetailWorker

urlpatterns = [
    path('', ListWorker.as_view()),
    path('<int:pk>/', DetailWorker.as_view()),
]