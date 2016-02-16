from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework.authtoken import views


urlpatterns = [
    url(r'^', include('board.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
]
