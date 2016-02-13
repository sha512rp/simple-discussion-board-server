from django.contrib.auth.models import User
from rest_framework import serializers
from models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Thread
        fields = ('id', 'title', 'created', 'author')


class UserSerializer(serializers.ModelSerializer):
    threads = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'threads')


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Message
        fields = ('id', 'message', 'created', 'author')
