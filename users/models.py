from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="email address",
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    )
    phone = models.CharField(
        max_length=15,
        unique=True,
        verbose_name="phone number",
        blank=True,
        null=True,
        help_text="Required. 15 characters or fewer. Letters, digits and + only.",
    )
    tg_nick = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="telegram nickname",
        blank=True,
        null=True,
        help_text="Required. 50 characters or fewer. Letters, digits and _ only.",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="avatar",
        help_text="Optional. Image file.",
    )
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="telegram chat id", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
