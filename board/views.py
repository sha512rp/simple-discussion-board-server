from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from board.models import Thread, Message
from board.serializers import ThreadSerializer, MessageSerializer, UserSerializer
from board.permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions


class ThreadList(APIView):
    """List all threads or create a new thread."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ThreadDetail(APIView):
    """Retrieve, update or delete a thread instance."""
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExists:
            raiseHttp404

    def get(self, request, pk, format=None):
        thread = self.get_object(pk)
        serializer = ThreadSerializer(thread)
        return Response(serializer.data)

    def put(self, request,pk, format=None):
        thread = self.get_object(pk)
        serializer = ThreadSerializer(thread, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        thread = self.get_object(pk)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, pk, format=None):
        """Add a new message to thread."""
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class MessageList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer
