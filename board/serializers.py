from django.contrib.auth.models import User
from rest_framework import serializers
from models import Thread


class ThreadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Thread
        fields = ('url', 'title', 'created', 'author')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')
