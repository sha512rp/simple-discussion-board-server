from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from board.models import Thread, Message
from board.serializers import ThreadSerializer, ThreadMsgSerializer, MessageSerializer, UserSerializer
from board.permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


class ThreadList(APIView):
    """List all threads or create a new thread."""

    def get(self, request, format=None):
        threads = Thread.objects.all()
        paginator = Paginator(threads, 10)
        page = request.GET.get('page')

        try:
            threads = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            threads = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            threads = paginator.page(paginator.num_pages)

        next_page = threads.next_page_number() if threads.has_next() else None
        prev_page = threads.previous_page_number() if threads.has_previous() else None
        serializer = ThreadSerializer(threads, many=True)
        return Response(dict(threads=serializer.data,
                             next=next_page,
                             prev=prev_page))

    def post(self, request, format=None):
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            msg_serializer = MessageSerializer(data=dict(text=request.data['text'],
                                                         thread=serializer.data['id']))
            if msg_serializer.is_valid():
                msg_serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ThreadDetail(APIView):
    """Retrieve, update or delete a thread instance."""
    
    def get_object(self, pk):
        try:
            return Thread.objects.get(pk=pk)
        except Thread.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        thread = self.get_object(pk)
        serializer = ThreadMsgSerializer(thread)
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
        thread = self.get_object(pk)
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            self.create_message(serializer, thread)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_message(self, serializer, thread):
        serializer.save(author=self.request.user,
                        thread=thread)



class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
