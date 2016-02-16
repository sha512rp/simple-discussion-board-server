from django.contrib.auth.models import User
from rest_framework import serializers
from models import Thread, Message
import hashlib


class UserSerializer(serializers.ModelSerializer):
    threads = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.all())
    gravatar_url = serializers.SerializerMethodField()

    def get_gravatar_url(self, obj):
        return "http://www.gravatar.com/avatar/" + hashlib.md5(obj.email.lower()).hexdigest()

    class Meta:
        model = User
        fields = ('id', 'username', 'threads', 'gravatar_url')


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    author = UserSerializer()
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all(), required=False)
    class Meta:
        model = Message
        fields = ('id', 'text', 'created', 'author', 'thread')
        depth = 1


class ThreadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    author = UserSerializer()
    messages = MessageSerializer(many=True, required=False)

    class Meta:
        model = Thread
        fields = ('id', 'title', 'created', 'author', 'messages')
        depth = 1
