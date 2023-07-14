from rest_framework.serializers import ModelSerializer 
from .models import Message
from loginapp.models import User

from rest_framework import serializers
from chat.models import *

class chatInboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = chat_inbox
        fields = ['sender', 'receiver', 'message', 'timestamp', 'socket_id']


class MessageSerializer(serializers.ModelSerializer):
    # sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp', "message_type"]


class PostMessageSerializer(serializers.ModelSerializer):
    # sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp',"socket_id"]