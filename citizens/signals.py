from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User

from .models import CitizenProfile


@receiver(post_save, sender=User)
def create_citizen_profile(sender, instance, created, **kwargs):

    if created and instance.role == User.Role.CITIZEN:
        CitizenProfile.objects.get_or_create(
            user=instance
        )