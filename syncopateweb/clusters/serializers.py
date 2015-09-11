from rest_framework import serializers
from .models import Cluster, Channel
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    clusters = serializers.PrimaryKeyRelatedField(many=True, queryset=Cluster.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'clusters')
 
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('group', 'topic', 'series_id')       

# REFERENCE
# http://www.django-rest-framework.org/api-guide/relations/
class ClusterSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #channels = serializersPrimaryKeyRelatedField(many=True, queryset=Channel.objects.all())
    channels = ChannelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cluster
        fields = ('name', 'api_key', 'token', 'owner', 'channels')

