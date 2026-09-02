from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        CITIZEN = "CITIZEN", "Citizen"
        OFFICER = "OFFICER", "Government Officer"
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Administrator"
        API_ADMIN = "API_ADMIN", "API Administrator"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.CITIZEN,
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
    )

    is_demo_user = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"