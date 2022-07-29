from rest_framework.routers import DefaultRouter
from lannister_auth.views import UserViewSet, RegisterUser
from rest_framework_simplejwt import views

from django.urls import path, re_path

urlpatterns = [
    re_path(r"^token/?", views.TokenObtainPairView.as_view(), name="jwt-obtain-token"),
    re_path(r"^refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
    path("register/", RegisterUser.as_view(), name="register-user"),
]

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
urlpatterns += router.urls
