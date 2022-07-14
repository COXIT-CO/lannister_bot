from django.urls import path

from .views import WorkerViewSet

urlpatterns = [
    path('', WorkerViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', WorkerViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'})),
]