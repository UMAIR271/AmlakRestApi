import requests
import json
from django.http import Http404
from Notifications.models import Notifications
from Notifications.serializer import NotificationsSerializer

def Push_notifications(title, body, user_id, type, data):
    try:
        print("Push Notification Generating")
        request_data = {
            "title":title,
            "body":body,
            "user_id":user_id,
            "type":type,
            "data":data
        }
        Notifications_Serializer =NotificationsSerializer(data=request_data)
        if Notifications_Serializer.is_valid(raise_exception=True):
            Notifications_Serializer.save()
        url = "https://fcm.googleapis.com/fcm/send"
        payload = json.dumps({
            "to": f"/topics/{user_id}",
            "priority": "high",
            "notification": {
                "title": title,
                "body": body,
            },
            "data" : {
                "type":type,
                "data":data         
            }
            })
        headers = {
        'Authorization': 'key=AAAAiVq9oWM:APA91bGVOV-DgflcrvktW-8f9n7TFku3gq1REH9obdJ2wGCSIFUFAxfQheIddopjarq4TOlsswivaZdwqDrlBZZmTKZkAz-p9jWG7BXSY3Zh_ZYz0vKofCvLxjL1i2YV0RZY_lqWRC7b',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response)
        return response

    except:
            return Http404