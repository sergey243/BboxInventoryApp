__author__ = 'dkarchmer@gmail.com'

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        Account = get_user_model()
        admin = Account.objects.filter(username='admin')
        if admin.objects.count() == 0:
            email = 'admin@site.com'
            username = 'admin'
            password = 'admin'
            admin = Account.objects.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()

        else:
            print('Admin accounts can only be initialized if no Accounts exist')