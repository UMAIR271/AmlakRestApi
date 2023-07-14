from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Notifications
from .serializer import NotificationsSerializer
import requests
import json



# type = "chat"
# type = "interest"
# type = "interested_request"




# Create your views here.


class FCMDeviceAuthorizedViewSet(APIView):
    def post(self, request):
        try:
            url = "https://fcm.googleapis.com/fcm/send"
            payload = json.dumps({
                "to": "/topics/127",
                "priority": "high",
                "notification": {
                    "title": "Push Notifications",
                    "body": "First Notification",
                    "text": "Text"
                }
                })
            headers = {
            'Authorization': 'key=AAAAiVq9oWM:APA91bGVOV-DgflcrvktW-8f9n7TFku3gq1REH9obdJ2wGCSIFUFAxfQheIddopjarq4TOlsswivaZdwqDrlBZZmTKZkAz-p9jWG7BXSY3Zh_ZYz0vKofCvLxjL1i2YV0RZY_lqWRC7b',
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            return Response({"message":response.text},status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class getNotification(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationsSerializer

    def get(self,request):
        id = request.user.id
        query =Notifications.objects.filter(user_id = id).values().order_by('-created_at')
        print(query)
        return Response(query)
        