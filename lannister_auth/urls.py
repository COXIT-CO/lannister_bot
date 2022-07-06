from rest_framework.routers import DefaultRouter
from lannister_auth.views import UserViewSet
from django.urls import path, include

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]

router = DefaultRouter()
router.register("lannister-users", UserViewSet)
urlpatterns += router.urls
