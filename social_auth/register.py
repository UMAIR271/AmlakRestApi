from django.contrib.auth import authenticate
from loginapp.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name, profile_image):
    print("profile", profile_image)
    filtered_user_by_email = User.objects.filter(email=email)
    print(filtered_user_by_email)
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('GOOGLE_CLIENT_SECRET'))
            print(filtered_user_by_email[0].auth_provider)
            return {
                'user_id': registered_user.id,
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name),
            'email': email,
            'password': os.environ.get('GOOGLE_CLIENT_SECRET'),
            }
        user = User.objects.create_user(**user)
        print(user, "user")
        user.is_verified = True
        user.auth_provider = provider
        user.profile_image = profile_image
        user.user_provider_id = user_id
        user.save()
        print("password", os.environ.get('GOOGLE_CLIENT_SECRET'))
        # print()
        new_user = authenticate(
            email=email, password=os.environ.get('GOOGLE_CLIENT_SECRET'))
        print(new_user, "hello")
        print(type(new_user))

        return {
            'user_id': new_user.id,
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }

def register_Apple_user(user_provider_id, name , email, provider, profile_image):
    filtered_user_by_email = User.objects.filter(user_provider_id=user_provider_id)
    if  filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(email=filtered_user_by_email[0].email, password = user_provider_id)
            print(filtered_user_by_email[0].auth_provider)
            return {
                'user_id': registered_user  .id,
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()
                }

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
    else:
        user = {
            'username': generate_username(name),
            'email': email,
            'password': user_provider_id,
            }
        user = User.objects.create_user(**user)
        print(user, "user")
        user.is_verified = True
        user.auth_provider = provider
        user.profile_image = profile_image
        user.user_provider_id = user_provider_id
        user.save()
        new_user = authenticate(email=email,  password = user_provider_id)
        return {
            'user_id': new_user.id,
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }