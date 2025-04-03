import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.EmailField(
        _("username"),
        max_length=250,
        unique=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
