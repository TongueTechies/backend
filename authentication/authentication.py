import typing as t
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from authentication.models import User as BaseUser, BlacklistedToken

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request: HttpRequest) -> tuple[BaseUser, dict[str, t.Any]]:
        access_token = self.get_token(request)
        if not access_token:
            return None
        try:
            payload = jwt.decode(
                access_token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Invalid token signature!")
        except Exception:
            raise ParseError()

        if self.is_token_blacklisted(payload):
            raise AuthenticationFailed("Invalid or expired token!")

        user = self.get_user(payload)
        if not user:
            raise AuthenticationFailed("Invalid user")

        return user, payload

    def get_token(self, request: HttpRequest) -> str | None:
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return None
        token_type, token = auth_header.split()
        if token_type != "Bearer":
            return None
        return token

    def is_token_blacklisted(self, payload) -> bool:
        return BlacklistedToken.objects.filter(token=payload).exists()

    def get_user(self, payload: dict[str, t.Any]) -> BaseUser | None:
        user_id = payload.get("user_id")
        if not user_id:
            return None
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user

    @classmethod
    def create_tokens(cls, user: BaseUser) -> tuple[str, str]:
        access_token_payload = {
            "user_id": str(user.id),
            "exp": int(
                (
                    datetime.now()
                    + timedelta(hours=settings.JWT_CONF["ACCESS_TOKEN_EXPIRY"])
                ).timestamp()
            ),
            "iat": datetime.now().timestamp(),
            "email": user.email,
        }

        access_token = jwt.encode(
            access_token_payload, key=settings.SECRET_KEY, algorithm="HS256"
        )

        refresh_token_payload = {
            "user_id": str(user.id),
            "exp": int(
                (
                    datetime.now()
                    + timedelta(days=settings.JWT_CONF["REFRESH_TOKEN_EXPIRY"])
                ).timestamp()
            ),
            "iat": datetime.now().timestamp(),
            "username": user.username,
            "refresh": True,
        }

        refresh_token = jwt.encode(
            refresh_token_payload,
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return access_token, refresh_token

    @classmethod
    def verify_token(cls, token: str, is_refresh_token=False) -> dict[str, t.Any]:
        try:
            payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        except (jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
            raise AuthenticationFailed("Invalid or expired token")
        except Exception:
            raise ParseError("Error decoding token")

        if is_refresh_token and not "refresh" in payload:
            raise AuthenticationFailed("Invalid token")

        return payload

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str:
        try:
            payload = cls.verify_token(refresh_token, is_refresh_token=True)
        except AuthenticationFailed:
            raise
        except Exception:
            raise ParseError()

        user_id = payload.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid user")

        access_token, _ = cls.create_tokens(user)
        return access_token
