from django.contrib.auth.models import User
from rest_framework import viewsets
from serializers import UserSerializer, ThreadSerializer
from models import Thread


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows threads to be viewed or edited.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
