from rest_framework import serializers
from .models import Cluster
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    clusters = serializers.PrimaryKeyRelatedField(many=True, queryset=Cluster.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'clusters')
        
class ClusterSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Cluster
        fields = ('name', 'api_key', 'token', 'owner')
