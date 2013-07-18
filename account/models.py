from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_contractor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
