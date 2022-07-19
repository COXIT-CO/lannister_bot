from rest_framework import generics
from lannister_auth.models import LannisterUser
from lannister_requests.models import BonusRequest
from .serializers import WorkerSerializer
from lannister_requests.serializers import BonusRequestBaseSerializer
from django.shortcuts import get_object_or_404


class ListWorker(generics.ListCreateAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer


class DetailWorker(generics.RetrieveUpdateDestroyAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer

    def get_object(self, *args, **kwargs):
        if self.kwargs.get("pk"):
            return get_object_or_404(LannisterUser, id=self.kwargs.get("pk"))

        return get_object_or_404(
            LannisterUser, slack_channel_id=self.kwargs.get("slack_channel_id")
        )


class ListWorkerRequest(generics.ListCreateAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestBaseSerializer


class DetailWorkerRequest(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestBaseSerializer
