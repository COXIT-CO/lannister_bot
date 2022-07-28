from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from lannister_auth.serializers import UserSerializer
from lannister_auth.models import LannisterUser, Role
from django.shortcuts import get_object_or_404


class RegisterUser(CreateAPIView):
    """
    View to allow user to register himself as worker by default.
    Or allow admin to register user and automatically grant him 'reviwer' and 'worker' roles
    """

    serializer_class = UserSerializer
    queryset = LannisterUser.objects.all()

    def create(self, request, *args, **kwargs):
        user_data = request.data
        if request.user.is_superuser:
            """
            If registered by admin, user will be reviewer and worker
            If registered by himself, user will be worker only
            """
            user = LannisterUser.objects.create_user(
                email=user_data.get("email"),
                username=user_data.get("username"),
                password=user_data.get("password"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
            )
            user.roles.set(["Reviewer", "Worker"])
            user.save()
            return Response(
                {
                    "response": "Registered successfully, please contact @lannister-bot with /register in your workspace to continue"
                },
                status=status.HTTP_201_CREATED,
            )
        user = LannisterUser.objects.create_user(
            email=user_data.get("email"),
            username=user_data.get("username"),
            password=user_data.get("password"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
        )
        if not user_data.get("roles"):
            user.roles.add(Role.objects.get(name="Worker"))
            user.save()
        return Response(
            {
                "response": "Registered successfully, please contact @lannister-bot with /register in your workspace to continue"
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(ModelViewSet):
    queryset = LannisterUser.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        try:
            # if int provided => look for id
            obj = int(self.kwargs.get("pk"))
            return get_object_or_404(LannisterUser, id=obj)
        except ValueError:
            # if string => look for username, 404 if None found
            obj = self.kwargs.get("pk")
            return get_object_or_404(LannisterUser, username=obj)
