from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # User login, detailed cluster list view
    url(r'^clusters/$', views.cluster_list, name='cluster-list'),

    # User login, detailed cluster single view
    url(r'^clusters/(?P<pk>[0-9]+)/$', views.cluster_detail, name='cluster-detail'),
    
    # Admin view only
    url(r'^users/$', views.UserList.as_view(), name='user-list'),

    # User login, concise cluster list view
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
