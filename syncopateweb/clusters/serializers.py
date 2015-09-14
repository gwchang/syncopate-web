from rest_framework import serializers
from .models import Cluster, Channel
from django.contrib.auth.models import User

class ClusterConciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('name', 'token', 'api_key', 'id')

class UserSerializer(serializers.ModelSerializer):
    #clusters = serializers.PrimaryKeyRelatedField(many=True, queryset=Cluster.objects.all())
    clusters = ClusterConciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'clusters')
 
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('group', 'topic')       

# REFERENCE
# http://www.django-rest-framework.org/api-guide/relations/
# https://docs.djangoproject.com/en/dev/topics/db/queries/#lookups-that-span-relationships
class ClusterDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #channels = serializersPrimaryKeyRelatedField(many=True, queryset=Channel.objects.all())
    channels = ChannelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cluster
        fields = ('name', 'token', 'api_key', 'owner', 'channels', 'id')

