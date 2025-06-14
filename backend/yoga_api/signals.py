from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update UserProfile when a User instance is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Ensure profile exists, useful if users were created before this signal
        # or if profile somehow got deleted.
        UserProfile.objects.get_or_create(user=instance)
        # If you have fields on UserProfile that need to be updated based on User model changes,
        # you can do that here. For now, just ensuring it exists.
        # instance.profile.save() # Not strictly necessary if just get_or_create
