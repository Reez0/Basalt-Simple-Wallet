from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .utils import get_user_from_token
from .serializers import LoginSerializer, MakePaymentSerializer, UserSerializer
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
import requests
from .models import Account, User
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
import json
import os

STELLAR_SERVER_URL = "https://horizon-testnet.stellar.org"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def dashboard(request):
    try:
        user = get_user_from_token(request)
        user_account = Account.objects.get(user=user)
        account_public_key = user_account.public
        server = Server(horizon_url=STELLAR_SERVER_URL)
        transactions = server.transactions().for_account(
            account_id=account_public_key).call()
        account = server.accounts().account_id(account_public_key).call()
        return Response(data={"success": True,
                              "data": {"transaction_history": transactions,
                                       "account": account}}, status=status.HTTP_200_OK)
    except PermissionDenied as e:
        return Response({"message": str(e)}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        return Response({"message": "Something went wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        return Response({"message": "Something went wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def make_payment(request):
    try:
        serializer = MakePaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors})
        server = Server(STELLAR_SERVER_URL)
        user = get_user_from_token(request)
        account = Account.objects.get(user=user)
        sender_secret_key = account.get_private_key()
        sender_keypair = Keypair.from_secret(sender_secret_key)
        sender_account = server.load_account(sender_keypair.public_key)
        base_fee = server.fetch_base_fee()
        transaction = (
            TransactionBuilder(
                source_account=sender_account,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=base_fee,
            )
            .append_payment_op(destination=serializer.validated_data['address'], asset=Asset.native(), amount=serializer.validated_data['amount'])
            .add_text_memo(serializer.validated_data['transaction_note'])
            .set_timeout(10)
            .build()
        )
        transaction.sign(sender_keypair)
        try:
            response = server.submit_transaction(transaction)
            return Response({"success": response['successful'], "message": f"Payment successful! A fee of {response['fee_charged']} lumens was charged."})
        except (BadRequestError, BadResponseError) as err:
            print(str(e))
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(str(e))
        return Response({"message": "Something went wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def add_credit(request):
    try:
        server = Server(STELLAR_SERVER_URL)
        user = get_user_from_token(request)
        account = Account.objects.get(user=user)
        sender_secret_key = os.getenv("ADMIN_PRIVATE_KEY")
        sender_keypair = Keypair.from_secret(sender_secret_key)
        sender_account = server.load_account(sender_keypair.public_key)
        print(sender_account)
        base_fee = server.fetch_base_fee()
        transaction = (
            TransactionBuilder(
                source_account=sender_account,
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=base_fee,
            )
            .append_payment_op(destination=account.public, asset=Asset.native(), amount="100")
            .add_text_memo(f"ACCOUNT CREDIT")
            .set_timeout(10)
            .build()
        )
        transaction.sign(sender_keypair)
        try:
            response = server.submit_transaction(transaction)
            return Response({"success": response['successful'], "message": f"Account credited successfully!"})
        except (BadRequestError, BadResponseError) as err:
            print(str(e))
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(str(e))
        return Response({"message": "Something went wrong, please try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
