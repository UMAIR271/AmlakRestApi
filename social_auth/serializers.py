from rest_framework import serializers
from . import apple
from . import google
from .register import register_social_user
import os
from rest_framework.exceptions import AuthenticationFailed



class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        print(user_data, "i love you")
        try:
            user_data['user_id']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        # if user_data['issued_to'] != os.environ.get('GOOGLE_CLIENT_ID'):
        #     print(os.environ.get('GOOGLE_CLIENT_ID'))
        #     print(user_data['issued_to'])
        #     raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['user_id']
        email = user_data['email']
        profile_image = user_data["picture"]
        if "name"in  user_data:
            name = user_data['name']
            provider = 'google'
            return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name, profile_image=profile_image)
        
        provider = 'google'
        name = ""
        return register_social_user(
            provider=provider, user_id=user_id, email=email, name= name, profile_image=profile_image)


class AppleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = apple.Apple.validate(auth_token)
        try:
            user_data
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        return user_data