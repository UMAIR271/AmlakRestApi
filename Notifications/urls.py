# from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from django.urls import path, include
from Notifications.views import FCMDeviceAuthorizedViewSet, getNotification


urlpatterns = [
    # Only allow creation of devices by authenticated users
    path('devices/', FCMDeviceAuthorizedViewSet.as_view(), name='create_fcm_device'),
    path('getNotification/', getNotification.as_view(), name='getNotification'),

    # ...
]