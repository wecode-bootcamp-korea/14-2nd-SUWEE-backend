import json
import jwt

from django.http import JsonResponse

from user.models import (
    User,
)
import my_settings


def check_auth_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers['Authorization']
            user_data    = jwt.decode(
                                    token,
                                    my_settings.SECRET_KEY['secret'],
                                    algorithm = my_settings.JWT_ALGORITHM,
                                )
            request.user = user_data["user_id"]

            return func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"message":"INVALID_TOKEN"}, status=400)

    return wrapper
