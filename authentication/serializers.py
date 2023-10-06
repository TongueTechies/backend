from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from authentication.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("email", "password", "confirm_password")

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password")
        validated_data["password"] = make_password(password)
        user = super(RegisterSerializer, self).create(validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
