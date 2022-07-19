from rest_framework import generics
from lannister_auth.models import LannisterUser
from lannister_requests.models import BonusRequest
from .serializers import WorkerSerializer
from lannister_requests.serializers import BonusRequestBaseSerializer


class ListWorker(generics.ListCreateAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer


class DetailWorker(generics.RetrieveUpdateDestroyAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer


class ListWorkerRequest(generics.ListCreateAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestBaseSerializer


class DetailWorkerRequest(generics.RetrieveUpdateDestroyAPIView):
    queryset = BonusRequest.objects.all()
    serializer_class = BonusRequestBaseSerializer
