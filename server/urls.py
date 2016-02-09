from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers
from board import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Easy to set up urls, because of viewsets
router.register(r'users', views.UserViewSet)
router.register(r'threads', views.ThreadViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
