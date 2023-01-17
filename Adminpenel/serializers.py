from rest_framework import serializers
from django.contrib.auth import get_user_model

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }