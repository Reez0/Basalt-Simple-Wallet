
from rest_framework.authtoken.models import Token
from rest_framework import authentication
from .models import User
from rest_framework.exceptions import PermissionDenied


class BearerAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'


def get_token(request):
    return request.META['HTTP_AUTHORIZATION'].split(' ')[1]


def get_user_from_token(request):
    try:
        token = get_token(request)
        user_token = Token.objects.get(key=token)
        user_id = user_token.user.id
        return User.objects.get(id=user_id)
    except Token.DoesNotExist:
        raise PermissionDenied("Invalid or expired token")
    except User.DoesNotExist:
        raise PermissionDenied("User not found for the given token")
    except Exception as e:
        print(e)
        raise PermissionDenied("Something went wrong")
