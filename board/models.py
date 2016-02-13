from __future__ import unicode_literals

from django.db import models


class Thread(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False)
    # url?
    author = models.ForeignKey('auth.User', related_name='threads')
    
    class Meta:
        ordering = ('created',)


#class User(models.Model):
#    username = models.CharField(max_length=30, blank=False)


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    # id, url, author?
    author = models.ForeignKey('auth.User', related_name='messages')
    
    class Meta:
        ordering = ('created',)

