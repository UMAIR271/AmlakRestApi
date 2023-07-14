from rest_framework.serializers import ModelSerializer 
from .models import *

class AppointmentSerilizer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'



class UserAppointmentSerilizer(ModelSerializer):
    class Meta:
        model = UserAvailabilty
        fields = '__all__'