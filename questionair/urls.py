from django.urls import path, include
from listing.views import *
from . import views
urlpatterns = [
    path('basic/question/', views.getQuestionView.as_view(), name="update_basic"),
    path('answer/', views.ListingAnswer.as_view(), name='user_question_view'),
    path('interested/', views.InterestedAnswer.as_view(), name='interested_view'),
    path('request/', views.RequestquestionView.as_view(), name='RequestquestionView'),
    path('getinterestedrequest/', views.getinterestedrequest.as_view(), name='getinterestedrequest'),
    path('getmyinterestedquestion/', views.getmyinterestedquestion.as_view(), name='getinterestedrequest'),
    path('isrequest/', views.isrequest.as_view(), name='isrequest'),
    path('getAllAttachedAnswer/', views.getAllAttachedAnswer.as_view(), name='getAllAttachedAnswer'),

]
