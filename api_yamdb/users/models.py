from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('us', 'user'),
        ('ad', 'admin'),
        ('md', 'moderator')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=150)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=USER_ROLES, default='user',
        max_length=2)