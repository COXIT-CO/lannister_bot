from lannister_roles.views import RoleViewSet
from django.urls import path

urlpatterns = [
    path("", RoleViewSet.as_view({'get': 'list'}), name="roles-list"),
    path("<pk>", RoleViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name="roles-single"),
]