from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Message)
admin.site.register(chat_inbox)
