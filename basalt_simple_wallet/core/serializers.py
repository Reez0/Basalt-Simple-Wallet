from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), username=email, password=password)

            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError(
                "Both email and password are required.")

        data['user'] = user
        return data


class MakePaymentSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    transaction_note = serializers.CharField(max_length=100, required=True)
    address = serializers.CharField(max_length=500, required=True)

    def validate(self, data):
        amount = data.get('amount')
        transaction_note = data.get('transaction_note')
        address = data.get('address')

        if amount and transaction_note and address:
            if amount <= 0:
                raise serializers.ValidationError(
                    'Amount must be greater than 0')
        else:
            raise serializers.ValidationError('All fields must be completed')

        return data
