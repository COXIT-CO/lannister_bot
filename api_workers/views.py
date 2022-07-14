from rest_framework import generics
from lannister_auth .models import LannisterUser
from lannister_slack .models import BonusRequest
from .serializers import WorkerSerializer
from .serializers import RequestSerializer


class ListWorker(generics.ListAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer


class DetailWorker(generics.ListAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer


class ListWorkerRequest(generics.ListCreateAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = RequestSerializer


class DetailWorkerRequest(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = RequestSerializer
