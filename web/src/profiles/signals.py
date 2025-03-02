from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, 
        first_name=instance.first_name,last_name=instance.last_name,
        email=instance.email )


@receiver(pre_save, sender=get_user_model())
def update_user_profile(sender, instance, **kwargs):  
    pass

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):  
    if instance.profile.first_name != instance.first_name or instance.profile.last_name != instance.last_name \
        or instance.profile.email != instance.email :
        if instance.profile.first_name != instance.first_name :
            instance.profile.first_name = instance.first_name
        if instance.profile.last_name != instance.last_name:
            instance.profile.last_name = instance.last_name
        if instance.profile.email != instance.email :
            instance.profile.email = instance.email

        instance.profile.save()



@receiver(post_save, sender=Profile)
def save_profile(sender, instance, **kwargs):
    user = instance.user
    if user.first_name != instance.first_name or user.last_name != instance.last_name:
        if user.first_name != instance.first_name:
            user.first_name = instance.first_name
        if user.last_name != instance.last_name:
            user.last_name = instance.last_name
        user.save()