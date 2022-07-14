from lannister_roles.views import RoleViewSet
from django.urls import path

urlpatterns = [
    path("roles/", RoleViewSet.as_view({'get': 'list'})),
    path("roles/<pk>", RoleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
]