from django.conf.urls import url
from board import views


urlpatterns = [
    url(r'^threads/$', views.thread_list),
    url(r'^threads/(?P<pk>[0-9]+)/$', views.snippet_detail),
]
