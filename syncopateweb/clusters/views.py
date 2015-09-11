#from django.shortcuts import render
#from django.http import HttpResponse

from .models import Cluster
from .serializers import ClusterSerializer
#from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

@login_required
@api_view(['GET', 'POST'])
def cluster_list(request, format=None):
    """
    List all clusters, or create a new cluster.
    """
    if request.method == 'GET':
        clusters = Cluster.objects.all()
        serializer = ClusterSerializer(clusters, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def cluster_detail(request, pk, format=None):
    """
    Retrieve, update or delete a cluster instance.
    """
    try:
        cluster = Cluster.objects.get(pk=pk)
    except Cluster.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClusterSerializer(cluster)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClusterSerializer(cluster, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cluster.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
