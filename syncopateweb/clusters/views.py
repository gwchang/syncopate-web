#from django.shortcuts import render
#from django.http import HttpResponse
from .models import Cluster, Channel
from django.contrib.auth.models import User
from .serializers import ClusterSerializer, UserSerializer, ChannelSerializer
from .permissions import HasValidAPIKey
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated

#@login_required
@api_view(['GET', 'POST'])
def cluster_list(request, format=None):
    """
    List all clusters, or create a new cluster.
    """
    #print(request.user)
    if request.method == 'GET':
        #clusters = Cluster.objects.all()
        # List all clusters owned by user
        #print(request.data.dict())
        clusters = Cluster.objects.filter(owner=request.user.id)
        serializer = ClusterSerializer(clusters, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create new cluster for user
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@login_required
@api_view(['GET'])
def cluster_detail_login(request, format=None):
    """
    Retrieve default login cluster instance.
    """
    queryset = Cluster.objects.filter(owner=request.user.id)
    if len(queryset) == 0:
        data = { 'detail' : 'Access forbidden' }
        return Response(data,status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'GET':
        pk_list = [ cluster.pk for cluster in queryset ]
        pk = max(pk_list)
        
        if len(pk_list) > 0:
            queryset = Cluster.objects.filter(pk=pk, owner=request.user.id)
            try:
                cluster = queryset.get()
            except Cluster.DoesNotExist:
                data = { 'detail' : 'Access forbidden' }
                return Response(data,status=status.HTTP_403_FORBIDDEN)

            serializer = ClusterSerializer(cluster)
            return Response(serializer.data)
        else:
            empty = {}
            return Response(empty)

@api_view(['POST'])
def authenticate(request, format=None):
    """
    Authentication process with Syncopate API
    """
    # Check token auth
    api_key = None
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    split = auth.split(' ')
    if split[0] == 'OAuth':
        api_key = split[1]

    if api_key is None:
        data = { 'detail' : 'No API key to authenticate.' }
        return Response(data,status=status.HTTP_403_FORBIDDEN)

    queryset = Cluster.objects.filter(api_key=api_key)
    try:
        cluster = queryset.get()
    except Cluster.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)
        data = { 'detail' : 'Access forbidden' }
        return Response(data,status=status.HTTP_403_FORBIDDEN)

    cid    = cluster.id
    group  = request.POST.getlist('group')[0]
    topics = request.POST.getlist('topic')
    for t in topics:
        chquery = Channel.objects.filter(cluster_id=cid, group=group, topic=t)
        if len(chquery) == 0:
            c = Channel.objects.create(cluster_id=cid, group=group, topic=t, series_id="")

    return Response(status=status.HTTP_204_NO_CONTENT)

#@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def cluster_detail(request, pk, format=None):
    """
    Retrieve, update or delete a cluster instance.
    """
    queryset = Cluster.objects.filter(pk=pk, owner=request.user.id)
    
    try:
        cluster = queryset.get()
    except Cluster.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)
        data = { 'detail' : 'Access forbidden' }
        return Response(data,status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = ClusterSerializer(cluster)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClusterSerializer(cluster, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(owner=request.user.id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cluster.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Admin view only
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


