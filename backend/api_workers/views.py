from rest_framework import generics, status
from rest_framework.response import Response
from lannister_auth.models import LannisterUser, Role
from lannister_requests.models import BonusRequest
from .serializers import WorkerSerializer
from lannister_requests.serializers import BonusRequestBaseSerializer
from django.shortcuts import get_object_or_404


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
        if self.kwargs.get("pk"):
            return get_object_or_404(LannisterUser, id=self.kwargs.get("pk"))

        return get_object_or_404(LannisterUser, username=self.kwargs.get("username"))

    def patch(self, request, *args, **kwargs):
        """
        TODO: Lock PATCH method under permission for admin only
        Pass integer as role
        """
        data = request.data
        user = LannisterUser.objects.get(username=self.kwargs.get("username"))
        provided_role = Role.objects.get(id=data.get("role"))
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
