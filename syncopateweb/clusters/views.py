#from django.shortcuts import render
#from django.http import HttpResponse

from .models import Cluster
from .serializers import ClusterSerializer
from rest_framework import generics

class ClusterList(generics.ListCreateAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer

class ClusterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
