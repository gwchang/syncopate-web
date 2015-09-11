from rest_framework import serializers
from .models import Cluster

class ClusterSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta:
        model = Cluster
        fields = ( 'name', 'api_key', 'token', 'owner' )
