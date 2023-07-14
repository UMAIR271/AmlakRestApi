from django.http import Http404
import uuid
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from questionair.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from loginapp.models import *
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Notifications.push_notification import Push_notifications
from chat.models import Message                                                   # Our Message model
from chat.serializers import * # Our Serializer Classes
# Users View                                                    # Decorator to make the view csrf excempt.
class chat_inbox_view(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = chatInboxSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get(self, request):
        try:
            user = request.user.id
            messages = chat_inbox.objects.filter(sender=user) | chat_inbox.objects.filter(receiver=user)
            data = messages.values()
            profile_list = []
            for i in data:
                chat_profile = {}
                if i["sender_id"] == user:
                    receiver = i["receiver_id"]   
                    user1=User.objects.filter(id = receiver).values().first()
                    username = user1["username"]
                    chat_profile["username"] = username
                    profile_image = user1["profile_image"]
                    chat_profile["profile_image"] = profile_image
                    chat_profile["chat_profile"] = i
                elif i["receiver_id"] == user:
                    sender = i["sender_id"]  
                    user1=User.objects.filter(id = sender).values().first()
                    username = user1["username"]
                    chat_profile["username"] = username
                    profile_image = user1["profile_image"]
                    chat_profile["profile_image"] = profile_image
                    chat_profile["chat_profile"] = i
                if chat_profile:
                    profile_list.append(chat_profile)
                
            return Response(profile_list)
        except chat_inbox.DoesNotExist:
            raise Http404
        
        




@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        serializer = PostMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



class message_list(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    parser_classes = (FormParser, MultiPartParser)

    def get(self,request, pk ):
        sender = request.user.id
        receiver = pk
        try:
            messages = Message.objects.filter(sender = sender, receiver = receiver ).order_by("-timestamp") | Message.objects.filter(sender = receiver, receiver = sender).order_by('-timestamp')                    
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            return JsonResponse(serializer.data, safe=False)
        except chat_inbox.DoesNotExist:
            raise Http404
    
    def post(self, request):
        sender = request.user.id
        request.data._mutable = True
        request.data["sender"] = sender
        data = request.data
        print(data)

        try:
            exit_message = Message.objects.filter(sender = sender,receiver =data['receiver']) | Message.objects.filter(sender = data['receiver'],receiver = sender)
            recevier_user = User.objects.filter(id = data['receiver']).values().first()
            print(exit_message,"1")
            if exit_message:
                # breakpoint()
                socket_id = exit_message.first().socket_id
                request.data['socket_id'] = socket_id
                request.data._mutable = False
                data = request.data
                serializer = PostMessageSerializer(data=data)
                if serializer.is_valid():
                    print("1234567891234")
                    serializer.save()

                chat_obj = chat_inbox.objects.filter(socket_id = socket_id).update(message = data['message'])
                print(chat_obj, "qwe")
                if chat_obj == 0:
                    print("tussef")
                    chat_serilizer = chatInboxSerializer(data=data)
                    if chat_serilizer.is_valid():
                        print("you")
                        chat_serilizer.save()
                # socket_id=var_1.socket_id
            else:
                socket_id = uuid.uuid4()
                data = request.data
                data["socket_id"] = socket_id
                request.data._mutable = False
                print(data)
                serializer = PostMessageSerializer(data=data)
                chat_serilizer = chatInboxSerializer(data=data)
                if serializer.is_valid():
                    print("love")
                    serializer.save()


                if chat_serilizer.is_valid():
                    print("you")
                    chat_serilizer.save()
            username = recevier_user["username"]
            title= "New Message Recevied"
            body = f"{username} send you a message"
            notification_data ={
                "sender_id": sender,
                "receiver_id": data['receiver'],
            }
            type = "chat"
            Push_notifications(title, body, data['receiver'], type, notification_data)
        except:
            print("hellllllllllllllllllllllllllllllo")
        return JsonResponse(request.data,status=201)
        