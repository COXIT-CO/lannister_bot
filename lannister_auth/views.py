from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from lannister_auth.serializers import UserSerializer
from lannister_auth.models import LannisterUser, Role


class RegisterUser(CreateAPIView):
    """
    View to allow user to register himself as worker by default.
    TODO: add different view for admin to register reviewer through API
    or check if jwt token was provided by the admin user => verify permission => perform register
    """

    serializer_class = UserSerializer
    queryset = LannisterUser.objects.all()

    def create(self, request, *args, **kwargs):
        user_data = request.data
        user = LannisterUser.objects.create_user(
            email=user_data.get("email"),
            username=user_data.get("username"),
            password=user_data.get("password"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
        )
        if not user_data.get("roles"):
            user.roles.add(Role.objects.get(id=1))
            user.save()
        # serializer = self.serializer_class(user)
        return Response(
            {
                "response": "Registered successfully, please contact @lannister-bot with /register in your workspace to continue"
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(ModelViewSet):
    queryset = LannisterUser.objects.all()
    serializer_class = UserSerializer
