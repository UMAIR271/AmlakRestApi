from django.urls import path, include
from  .views import *
from . import views
urlpatterns = [
      path('signup/', SignupView.as_view(), name='signup'),
      path('login/', LoginView.as_view(), name='login'),    

]
