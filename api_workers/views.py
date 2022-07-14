from rest_framework import generics
from lannister_auth .models import LannisterUser
from .serializers import WorkerSerializer


class ListWorker(generics.ListAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer


class DetailWorker(generics.ListAPIView):
    queryset = LannisterUser.objects.all()
    serializer_class = WorkerSerializer

