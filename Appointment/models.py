from django.db import models
from loginapp.models import User
from listing.models import *


# Create your models here.

class Appointment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Appointment')
    appointment_Date = models.DateField(auto_now_add=False)
    appointment_Time = models.TimeField(auto_now_add=False)
    listing_id = models.ForeignKey(listing, related_name="ListingId", on_delete=models.CASCADE, null = True)
    Listing_Owner_Id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ListingOwnerId", on_delete=models.CASCADE, null = True)
    is_Confirmed = models.BooleanField(default=False)
    status = models.CharField(default = "pending", max_length=300)
    createdDateTime = models.DateTimeField(auto_now_add=True)


class UserAvailabilty(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='UserAvailabilty')
    start_Date = models.DateField(auto_now_add=False)
    end_Date = models.DateField(auto_now_add=False)
    start_Time = models.TimeField(auto_now_add=False)
    end_Time = models.TimeField(auto_now_add=False)