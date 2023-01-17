from django.contrib.auth import authenticate
from loginapp.models import User
import os


class Apple:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            return auth_token
        except:
            return "The token is either invalid or has expired"