from django.shortcuts import render, redirect
from django.template import Context
from django.http import HttpResponseRedirect
#from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Cluster, Channel
from django.contrib.auth.models import User
from .serializers import ClusterDetailSerializer, ClusterConciseSerializer, UserSerializer, ChannelSerializer
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .utils import genToken
from .forms import NewClusterForm
import hashlib, random

@login_required
def index(request):
    clusters = Cluster.objects.filter(owner=request.user.id)
    form = NewClusterForm()
    if len(clusters) == 0:
        return render(request, 'clusters/index.html', {'nocluster':True,'form':form})
    serializer = ClusterConciseSerializer(clusters[len(clusters)-1])
    return render(request, 'clusters/index.html', {'cluster':serializer.data,'form':form})

@api_view(['POST'])
def cluster_new(request, format=None):
    form = NewClusterForm(request.POST)
    if form.is_valid():
        randomkey = hashlib.md5(str(random.getrandbits(256))).hexdigest();
        token = genToken(randomkey)
        cluster = Cluster.objects.create(name=form.cleaned_data['name'],api_key=randomkey,token=token,owner=request.user)
    
    return redirect('/clusters')

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
        serializer = ClusterConciseSerializer(clusters, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # Create new cluster for user
        serializer = ClusterConciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@login_required
@api_view(['GET'])
def cluster_login(request, format=None):
    """
    Retrieve default login cluster instance.
    """
    queryset = Cluster.objects.filter(owner=request.user.id)
    if len(queryset) == 0:
        data = { 'detail' : 'Access forbidden' }
        return Response(data,status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'GET':
        pk_list = [ cluster.pk for cluster in queryset ]
        
        if len(pk_list) > 0:
            pk = max(pk_list)
            queryset = Cluster.objects.filter(pk=pk, owner=request.user.id)
            try:
                cluster = queryset.get()
            except Cluster.DoesNotExist:
                data = { 'detail' : 'Access forbidden' }
                return Response(data,status=status.HTTP_403_FORBIDDEN)

            serializer = ClusterDetailSerializer(cluster)
            return Response(serializer.data)
        else:
            empty = {}
            return Response(empty)

@api_view(['POST'])
def cluster_sync(request, format=None):
    """
    Sync process with Syncopate API client
    """
    # Check token auth
    api_key = None
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    split = auth.split(' ')
    print auth
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
            c = Channel.objects.create(cluster_id=cid, group=group, topic=t)

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
        serializer = ClusterDetailSerializer(cluster)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ClusterDetailSerializer(cluster, data=request.data)
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


