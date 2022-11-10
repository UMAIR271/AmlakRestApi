from django.urls import path, include
from chat.views import *
urlpatterns = [
    # URL form : "/api/messages/1/2"
    path('api/get_chat/<int:pk>/', message_list.as_view(), name='message-detail'),
    path('api/get_chat_inbox/', chat_inbox_view.as_view(), name='message'),  # For GET request.
      # For GET request.
    # URL form : "/api/messages/"
    path('api/send_messages/', message_list.as_view(), name='message-list'),
    # path('api/get_messages/', message_list.as_view(), name='message-list'),   # For POST
       # For POST
    # URL form "/api/users/1"
]