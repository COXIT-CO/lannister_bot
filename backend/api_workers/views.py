from rest_framework import generics, status
from rest_framework.response import Response
from lannister_auth.models import LannisterUser, Role
from lannister_requests.models import BonusRequest
from .serializers import WorkerSerializer
from lannister_requests.serializers import BonusRequestBaseSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import MultipleObjectsReturned


class ListWorkers(generics.ListCreateAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer

    def get_queryset(self):
        # very stupid way of getting optional url, refactor it later with smarter drf tools
        if self.kwargs.get("reviewers"):
            return LannisterUser.objects.filter(roles__in=[2])
        return self.queryset.all()


class DetailWorker(generics.RetrieveUpdateDestroyAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer

    def get_object(self, *args, **kwargs):
        """
        Parsing object by model id or slack_channel_id
        """
        print(self.kwargs)
        if self.kwargs.get("pk"):
            return get_object_or_404(LannisterUser, id=self.kwargs.get("pk"))
        if self.kwargs.get("username"):
            return get_object_or_404(
                LannisterUser, username=self.kwargs.get("username")
            )

        # handles events from slack, they're mad buggy
        if self.kwargs.get("channel_id"):
            try:
                return get_object_or_404(
                    LannisterUser, slack_channel_id=self.kwargs.get("channel_id")
                )
            except (MultipleObjectsReturned, ValueError):  # only for debug/showcase
                return LannisterUser.objects.filter(
                    slack_channel_id=self.kwargs.get("channel_id")
                ).first()

    def patch(self, request, *args, **kwargs):
        """
        TODO: Lock PATCH method under permission for admin only
        Pass integer as role
        """
        data = request.data
        user = LannisterUser.objects.get(username=self.kwargs.get("username"))

        if (
            data.get("slack_channel_id") and len(data) == 1
        ):  # /register request comes here
            user.slack_channel_id = data.get("slack_channel_id")
            user.save()
            return Response(status=status.HTTP_200_OK)

        if data.get("slack_user_id") and len(data) == 1:  # /register request comes here
            user.slack_user_id = data.get("slack_user_id")
            user.save()
            return Response(status=status.HTTP_200_OK)

        provided_role = Role.objects.get(name=data.get("role"))
        user.roles.remove(provided_role)
        return Response(
            data={"response": "User was unassigned successfully"},
            status=status.HTTP_200_OK,
        )


class ListWorkerRequest(generics.ListCreateAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestBaseSerializer


class DetailWorkerRequest(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestBaseSerializer
