from django.contrib import admin

from .models import Cluster, Channel

class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 3

class ClusterAdmin(admin.ModelAdmin):
    inlines = [ChannelInline]
    list_display = ('name', 'api_key', 'token')

admin.site.register(Cluster, ClusterAdmin)
