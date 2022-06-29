from rest_framework.viewsets import ModelViewSet
from lannister_auth.serializers import UserSerializer
from lannister_auth.models import LannisterUser


class UserViewSet(ModelViewSet):
    queryset = LannisterUser.objects.all()
    serializer_class = UserSerializer
