from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
           }

class LoginView(APIView):
    # authentication_classes = (JWTTokenUserAuthentication)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request, email=serializer.validated_data['email'],
            password=serializer.validated_data['password'])
        if user is not None and user.is_staff:
            token = get_tokens_for_user(user)
            return Response({'token': token})
        else:
            return Response({'error': 'Invalid login credentials'}, status=401)



class SignupView(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        User = get_user_model()
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        new_user = User.objects.create_user(username=username, password=password, email=email)
        refresh_token = RefreshToken.for_user(new_user)
        token = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token),
        }
        return Response({'token': token})