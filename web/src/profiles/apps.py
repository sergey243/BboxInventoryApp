from django.apps import AppConfig

class profilesConfig(AppConfig):
    name = 'profiles'
    def ready(self):
        from .signals import create_user_profile, save_profile, save_user_profile,update_user_profile
