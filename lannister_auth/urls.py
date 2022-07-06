from rest_framework.routers import DefaultRouter
from lannister_auth.views import UserViewSet, RegisterUser
from rest_framework_simplejwt import views

from django.urls import path, include, re_path

urlpatterns = [
    path("", include("djoser.urls")),
    re_path(r"^token/?", views.TokenObtainPairView.as_view(), name="jwt-obtain-token"),
    re_path(r"^refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
    # path("", include("djoser.urls.jwt")),
    path("register/", RegisterUser.as_view(), name="register-user"),
]

router = DefaultRouter()
router.register("lannister-users", UserViewSet)
urlpatterns += router.urls
