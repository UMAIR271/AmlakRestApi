from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from io import BytesIO
from PIL import Image
from django.core.files import File

from PIL import Image

from Amlaq import settings
# Create your models here.

def compress(image):
    print("hello")
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=60) 
    new_image = File(im_io, name=image.name)
    return new_image
class Amenities(models.Model):
    AMENITIES = (
        ("Dishwasher","Dishwasher"),
        ("Fireplace","Fireplace"),
        ("Swimming pool","Swimming pool"),
    )
    Amenities_Name = models.CharField(max_length=50, null=True)
    Cration_Time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        # data = {"id": self.id, "Amenities_Name": self.Amenities_Name }
        return str(self.id)


class listing(models.Model):
    zero = 0
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5 
    six = 6
    saven = 7 
    TYPE_CHOIES = (
        ("Residential" , "Residential"),
        ("Commercial" , "Commercial"),
    )
    Purpose_Choies = (
        ("Sell","Sell"),
        ("Rent","Rent"),
    )
    STATUS_CHOICES = (
    (zero, 'zero'),
    (one, 'one'),
    (two, 'two'),
    (three, 'three'),
    (four, 'four'),


    )
    PROPERTY_TENURE = (
        ("FreeHold","FreeHold"),
        ("Non FreeHold","Non FreeHold"),
        ("LeaseHold","LeaseHold"),
    )
    OCCUPANCY = (
        ("Owner occupied","Owner occupied"),
        ("Investment","Investment"),
        ("Vacant","Vacant"),
        ("Tenanted","Tenanted"),
    )
    PROJECT_STATUS = (
        ("Off plan","Off plan"),
        ("Completed","Completed"),
    )
    RENOVATION_TYPE = (
        ("Fully upgraded","Fully upgraded"),
        ("Partially upgraded","Partially upgraded"),
    )
    FINANCIAL_STATUS = (
        ("Mortgaged","Mortgaged"),
        ("Cash","Cash"),
    )
    FURNISHED_TYPE = (
        ( 'Unfurnished', 'Unfurnished'),
        ('Semi-furnished','Semi-furnished'),
        ('Furnished','Furnished')

    )
    PROPERTY_USAGE = (
        ("Single Family","Single Family"),
        ("Bachelors","Bachelors")
    )
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user", on_delete=models.CASCADE,)
    Title = models.CharField(max_length=50)
    Descriptions = models.CharField(max_length=300)
    Type = models.CharField(max_length=11, choices=TYPE_CHOIES)
    Purpose_Type = models.CharField(max_length=13, choices=Purpose_Choies)
    Bedrooms = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    Batrooms = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    Furnishing_type = models.CharField(max_length=14, choices=FURNISHED_TYPE ,null=True)
    Property_Tenure = models.CharField(max_length=13, choices=PROPERTY_TENURE, null=True)
    size = models.CharField(max_length=300)
    Build_up_Area = models.CharField(max_length=300)
    parking_number = models.CharField(max_length=300)
    Property_Developer = models.CharField(max_length=300)
    Build_year = models.CharField(max_length=300)
    Building_Floor = models.CharField(max_length=300)
    Floor_number = models.CharField(max_length=300)
    Dewa_number =  models.CharField(max_length=300)
    Occupancy = models.CharField(max_length=14, choices=OCCUPANCY)
    Project_status = models.CharField(max_length=9, choices=PROJECT_STATUS)
    Renovation_type = models.CharField(max_length=18, choices=RENOVATION_TYPE)
    Layout_type = models.CharField(max_length=300)
    property_pricing  = models.CharField(max_length=300)
    Service_charge  = models.CharField(max_length=300)
    financial_status = models.CharField(max_length=9, choices=FINANCIAL_STATUS)
    Cheques = models.IntegerField(max_length=1, choices=STATUS_CHOICES)
    property_location = models.CharField(max_length=300)
    street_Address = models.CharField(max_length=300)
    project_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now=True)
    list_verified = models.BooleanField(default=False, null=True)
    latitude = models.FloatField(max_length=300, null=True)
    longitude = models.FloatField(max_length=300, null=True)
    property_usage = models.CharField(max_length=13, choices=PROPERTY_USAGE, null=True)
    cover_image = models.CharField(max_length=1000, null=True)




class Property_Type(models.Model):
    Property_Choices = (
        ('Apartment' , 'Apartment'),
        ('Bungalow' , 'Bungalow'),
        ('Compound' , 'Compound'),
        ('Duplex' , 'Duplex'),
        ('Full floor' , 'Full floor'),
        ('Half floor' , 'Half floor'),
        ('Land' , 'Land'),
        ('Pent House' , 'Pent House'),
        ('Town House' , 'Town House'),
        ('Villa' , 'Villa'),
        ('Whole Building' , 'Whole Building'),
        ('Hotel apartments' , 'Hotel apartments'),
        ('Bulk units' , 'Bulk units'),
    )
    listing = models.ForeignKey(listing, related_name="property", on_delete=models.CASCADE )
    property_type = models.CharField(max_length=16, choices=Property_Choices )
    def __str__(self) -> str:
        return (self.property_type)

class userprofile(models.Model):
    userprofile = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userprofiledata", on_delete=models.CASCADE, )
    listing = models.ForeignKey(listing, related_name="userlisting", on_delete=models.CASCADE, )
    profile_image = models.ImageField(upload_to ='uploads/')

class Listing_Media(models.Model):
    images_Url = models.ImageField(upload_to ='uploads/')
    listing = models.ForeignKey(listing, related_name="list", on_delete=models.CASCADE )


    def __str__(self) -> str:
        return (self.images_Url.url)

class floorPlane(models.Model):
    floorPlaneImage = models.ImageField(upload_to ='uploads/')
    listing = models.ForeignKey(listing, related_name="floorplane", on_delete=models.CASCADE )


    def __str__(self) -> str:
        return (self.floorPlaneImage)

class property_verification(models.Model):
    propertyVerificationImage = models.ImageField(upload_to ='uploads/')
    listing = models.ForeignKey(listing, related_name="propertyVerificationImage", on_delete=models.CASCADE )


    def __str__(self) -> str:
        return (self.propertyVerificationImage)

class compress_image(models.Model):
    images_path = models.ImageField(upload_to ='compress/',  verbose_name=_("Photo"))
    listing = models.ForeignKey(listing, related_name="compress", on_delete=models.CASCADE )

    def save(self, *args, **kwargs):
        instance = super(Photo, self).save(*args, **kwargs)
        image = Image.open(instance.images_path.path)
        image.save(instance.images_path.path,quality=20,optimize=True)
        return instance                                                                                                                                                                                                                                                                                                                      



class interested(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   listing = models.ForeignKey(listing, on_delete=models.CASCADE, null=True, blank=True)
   created_at = models.DateTimeField(auto_now=True)
   is_interested = models.BooleanField(default=False)
   
   def __str__(self) -> str:
        return str(self.user)

class Listing_Amenities(models.Model):
    listing = models.ForeignKey(listing, related_name="Amenities", on_delete=models.CASCADE)
    Amenities_ID = models.ForeignKey("Amenities", related_name="Amenities_ID",on_delete=models.CASCADE, null= True)
    Cration_Time = models.DateTimeField(auto_now_add=True)



class Appointment(models.Model):
    NULL = 'null'
    APPROVED = 'approved'
    DECLINE = 'declined'
    STATUS = (
        (NULL, _('Null')),
        (APPROVED, _('Approved')),
        (DECLINE, _('Decline')),
    )
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="first_user")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="second_user")
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS, default=NULL)


    def __str__(self):
        return self.status


class AvailableSlots(models.Model):
    AVAILABLE = 'available'
    BOOKED = 'booked'
    SLOT_STATUS = (
        (AVAILABLE, _('Available')),
        (BOOKED, _('Booked')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    time_slots = models.TimeField()
    slot_status = models.CharField(max_length=50, choices=SLOT_STATUS)
    
    def __str__(self):
        return self.slot_status

