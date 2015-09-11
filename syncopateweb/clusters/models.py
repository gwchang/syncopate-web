from django.contrib.auth.models import User
from django.db import models

class Cluster(models.Model):
    name    = models.CharField(max_length=200)  # Human readable name
    api_key = models.CharField(max_length=200)  # Publish/upload key
    token   = models.CharField(max_length=200)  # Subscription key
    owner   = models.ForeignKey(User, related_name='clusters')

class Channel(models.Model):
    cluster     = models.ForeignKey(Cluster)        # Cluster than channel belongs to
    group       = models.CharField(max_length=200)  # Group of channel
    topic       = models.CharField(max_length=200)  # Topic of channel
    series_id   = models.CharField(max_length=200)  # Series id of channel
