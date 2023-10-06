from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
