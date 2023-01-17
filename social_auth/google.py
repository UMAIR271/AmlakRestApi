from google.auth.transport import requests
from google.oauth2 import id_token
import requests
import json


class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            print(auth_token)
            authorization = "Bearer" + " " + auth_token
            headers = {
            'Authorization': authorization,
            'Content-Type': 'application/json'
            }
            # id_token_url = "https://www.googleapis.com/oauth2/v1/tokeninfo?id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6IjAyYTYxZWZkMmE0NGZjMjE1MTQ4ZDRlZmZjMzRkNmE3YjJhYzI2ZjAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDE4MjMzMjMxNTI3LWx2NzVwbTNwc3Q0dXNlN3MzMHZkN3JkOW5rMThsdGIyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAxODIzMzIzMTUyNy1sdjc1cG0zcHN0NHVzZTdzMzB2ZDdyZDluazE4bHRiMi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwNjQyMzc5MzY3MjIyMDExNzA3NCIsImVtYWlsIjoibWFsaWt1bWFpcjI3MDFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJ3RmRJZUJ0WVNHaXQ2N0gyTTkyOV93IiwiaWF0IjoxNjcyNDE3NDE1LCJleHAiOjE2NzI0MjEwMTV9.UqbPRNsgBaGsuFxnTEmXv8zrRXb-wee62ExPEu-EDS3GpUZxz14WbyuDLXrkQXCycTL3FCnhbsfGMhWI4SqgOexZbgL7tSAkMyND82J1gk-9wVkuMWUL52IxS-qRWn7WWcJf8yT9lWrhF7nfmAKM4UsMFWPT9_fbBeC44A8O4QQ215xfNTA7dYfkQvyEfEtD1C-BSFqzBBhsChjfKi6Q1-A4SsK9ynU0aJ6zgW0PGA2xgMmn2MHEu6vYwXRa7dlSxh7-EYmeBQlWqR50Vy3GD7ZfpvfolMVVsgDzsMBzTm-X-ogWTK0B9SoJqwlRbk6alSLOO2lXxYmDdbWRtCD_2g"
            url = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+auth_token
            response = requests.request("POST",url)
            if response.ok == True:
                change_type =json.loads(response.text)
                profile_url= "https://www.googleapis.com/oauth2/v1/userinfo"
                profile_response = requests.request("GET", profile_url, headers=headers)
                change_type1 =json.loads(profile_response.text)
                dict_3=dict(change_type,**change_type1)
                return dict_3
            # idinfo = id_token.verify_oauth2_token(
            #     auth_token, requests.Request())
            # print(idinfo.keys)
            # if 'accounts.google.com' in idinfo['iss']:
            #     return idinfo

        except:
            return "The token is either invalid or has expired"