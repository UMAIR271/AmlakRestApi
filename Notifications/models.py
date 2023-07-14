from django.db import models
from loginapp.models import User
# Create your models here.
class Notifications(models.Model):
    title = models.CharField(max_length=1000)
    body =models.CharField(max_length=1000)
    type =models.CharField(max_length=1000)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push')
    data =models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
