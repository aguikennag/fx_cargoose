from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Settings


@receiver(post_save, sender=get_user_model())
def create_user_related(sender, instance, created, **kwargs):
    pass
