from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.ClusterList.as_view(), name='cluster-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ClusterDetail.as_view(), name='cluster-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
