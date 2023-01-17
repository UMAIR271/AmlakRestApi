from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import *
from loginapp.models import User
from django.contrib.auth import authenticate
from .register import generate_username, register_Apple_user
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

# AppleSocialAuthView
@method_decorator(csrf_exempt, name='dispatch')
class AppleSocialAuthView(GenericAPIView):

    serializer_class = AppleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """
        data = request.data
        user_provider_id = data["socialUserId"]
        for key, value in data.iteritems() :
            print(key, value)
        if data["name"]:
            # name = data["name"]
            print("allah ho")
            # email = data["email"]
            # print(email)
        provider = "apple"
        profile_image="uploads/dipika_0ApZvQu.jpg"
        print(data)
        # data= register_Apple_user(provider, user_provider_id, email, name, profile_image)
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
