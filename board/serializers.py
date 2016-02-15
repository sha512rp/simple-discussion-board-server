from django.contrib.auth.models import User
from rest_framework import serializers
from models import Thread, Message


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all(), required=False)
    class Meta:
        model = Message
        fields = ('id', 'text', 'created', 'author', 'thread')
        depth = 1


class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    messages = MessageSerializer(many=True, required=False)

    class Meta:
        model = Thread
        fields = ('id', 'title', 'created', 'author', 'messages')
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    threads = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'threads')
