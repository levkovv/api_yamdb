from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator')
    )
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=USER_ROLES, default='user',
        max_length=9)
