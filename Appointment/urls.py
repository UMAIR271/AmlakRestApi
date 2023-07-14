from django.urls import path, include
from .views import *
urlpatterns = [
    path('create/', AppointmentView.as_view(), name='appointment'),
    path('UserAvailabilty/', UserAvailabiltyView.as_view(), name='UserAvailabilty'),
    path('getUserAvailabilty/', getUserAvailabilty.as_view(), name='getUserAvailabilty'),
    path('Updateappointment/', UpdateAppointmentView.as_view(), name='Updateappointment'),
    path('GetMySentAppointment/', GetMySentAppointment.as_view(), name='GetMySentAppointment'),
    path('getAvailableTimeSlot/', getAvailableTimeSlot.as_view(), name='getAvailableTimeSlot'),
    path('GetRecviedAppointmentRequest/', GetRecviedAppointmentRequest.as_view(), name='GetRecviedAppointmentRequest'),
    # path('UserAvailabilty/', AvailabiltyView.as_view(), name='UserAvailabilty'),
]