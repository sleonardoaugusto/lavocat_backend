import json

import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from lavocat.core.models import UserAllowed

GOOGLE_AUTH_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'


class Unauthorized(Exception):
    pass


class UserNotAllowed(Exception):
    pass


def authenticate(email):
    user = UserAllowed.objects.filter(email=email)

    if not user.exists():
        raise UserNotAllowed

    user = User.objects.get(email=email)

    token = RefreshToken.for_user(user)
    return {
        'useremail': user.email,
        'access_token': str(token.access_token),
        'refresh_token': str(token),
    }


def google_auth(token):
    payload = {'access_token': token}
    r = requests.get(GOOGLE_AUTH_URL, params=payload)

    if r.status_code == status.HTTP_401_UNAUTHORIZED:
        raise Unauthorized

    data = json.loads(r.text)

    user_email = data['email']
    return authenticate(user_email)
