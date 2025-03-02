from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from profiles.models import Profile

class Command(BaseCommand):
    help = 'Create profiles for all the user not having one'
    
    def handle(self, *args, **kwargs):
        user_model = get_user_model()
        users = user_model.objects.all().select_related('profile')
        count = 0
        for user in users:
            profile = Profile.objects.filter(user=user).first()
            if not profile:
                profile = Profile.objects.create(user=user,email=user.email,first_name=user.first_name,
                last_name=user.last_name)
                profile.save()
                count += 1
        print('{} user(s) profile(s) created'.format(str(count))) 