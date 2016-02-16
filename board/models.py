from __future__ import unicode_literals

from django.db import models


class Thread(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey('auth.User', related_name='threads')
    
    class Meta:
        ordering = ('created',)


class Message(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey('auth.User', related_name='messages')
    thread = models.ForeignKey(Thread, related_name='messages')
    
    class Meta:
        ordering = ('created',)

