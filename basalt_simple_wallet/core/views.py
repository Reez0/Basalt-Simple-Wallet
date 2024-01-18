from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import get_user_from_token
from .serializers import LoginSerializer, UserSerializer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from stellar_sdk import Server, Keypair, TransactionBuilder, Network
import requests
from .models import Account, User
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

STELLAR_SERVER_URL = "https://horizon.stellar.org"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def dashboard(request):
    try:
        user = get_user_from_token(request)

        return Response(data={"success": True, "message": "Hello, world!"}, status=status.HTTP_200_OK)
    except PermissionDenied as e:
        return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"message": "Something with wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_account(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            keypair = Keypair.random()
            response = requests.get(
                f"https://friendbot.stellar.org?addr={keypair.public_key}")
            if response.status_code == 200:
                instance = serializer.save()
                user = User.objects.get(id=instance.id)
                account = Account(user=user,
                                  public=keypair.public_key)
                account.save_private_key(keypair.secret)
                account.save()
                return Response(data={"success": True, "message": f"Welcome, {serializer.data['first_name']}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": "Something with wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "data": {
                    "token": token.key,
                    "email": user.email
                }, "message": f"Logged in successfully. Welcome back, {user.first_name}!",

            }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something with wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
