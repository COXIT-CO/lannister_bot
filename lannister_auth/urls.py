from rest_framework.routers import DefaultRouter
from lannister_auth.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
urlpatterns = router.urls
