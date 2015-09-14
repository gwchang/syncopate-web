from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # Syncopate client authentication
    url(r'^cluster-sync/$', views.cluster_sync, name='cluster-sync'),

    # User login, detailed cluster list view
    url(r'^cluster-list/$', views.cluster_list, name='cluster-list'),

    # User login, default login cluster view
    url(r'^cluster-login/$', views.cluster_login, name='cluster-login'),

    # User login, detailed cluster single view
    url(r'^cluster/(?P<pk>[0-9]+)/$', views.cluster_detail, name='cluster-detail'),
    
    # Admin view only
    url(r'^user/$', views.UserList.as_view(), name='user-list'),

    # User login, concise cluster list view
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
