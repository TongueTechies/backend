from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import BlacklistedToken
from authentication.models import User as BaseUser
from authentication.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from utils.responses import CustomResponse as cr

from .authentication import JWTAuthentication as jwt_auth

User = get_user_model()


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("confirm_password")
        user = serializer.save()

        access_token, refresh_token = jwt_auth.create_tokens(user)
        return cr.success(
            data={"access_token": access_token, "refresh_token": refresh_token},
            message="User registered successfully!",
            status_code=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return cr.error(
                message="Invalid credentials provided",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        access_token, refresh_token = jwt_auth.create_tokens(user)

        return cr.success(
            data={"access_token": access_token, "refresh_token": refresh_token},
            message="User logged in successfully!",
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request: Request) -> Response:
        user = BaseUser.objects.filter(pk=request.user.id).first()
        serializer = self.serializer_class(instance=user)
        if not user:
            return cr.error(
                message="User not found!", status_code=status.HTTP_403_FORBIDDEN
            )
        return cr.success(data=serializer.data, message="Profile fetched successfully!")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        BlacklistedToken.objects.create(token=request.auth)
        return cr.success(message="User logged out successfully!")
