from django.conf.urls import url, include
from django.contrib.auth.models import User


urlpatterns = [
    url(r'^', include('board.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
