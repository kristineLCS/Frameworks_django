from django.db.models.signals import post_save #This gets fired when a user is created
from django.contrib.auth.models import User #The user model will be the sender
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
   instance.profile.save()

for user in User.objects.all():
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)