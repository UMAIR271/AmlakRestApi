from django.db import models
from loginapp.models import User
import uuid
# Create your models here.
from django.conf import settings
from django.core.cache import cache


class chat_inbox(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_id')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_id')
    message = models.CharField(max_length=1200, null = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    socket_id = models.UUIDField(editable = True, null = True)
    


class Message(models.Model):
    socket_id = models.UUIDField(editable = True, null = True)
    message_type = models.CharField(max_length=1200 ,default = "text" )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)