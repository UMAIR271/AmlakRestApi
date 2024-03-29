from google.auth.transport import requests
from google.oauth2 import id_token
import requests

class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+auth_token
        response = requests.request("POST", url)
        print(response)

        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo

        except:
            return "The token is either invalid or has expired"