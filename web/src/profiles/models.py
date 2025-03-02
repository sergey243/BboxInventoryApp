import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from app.settings import MEDIA_ROOT


GENDER =(('man',_(u'Man')),('woman',_(u'Woman')))

def upload_user_data(instance, filename):
    return os.path.join(MEDIA_ROOT,'user_%d' % instance.user_id.id, filename)

'''
This model represent the model for all the user profiles
'''
class Profile(models.Model):
    user       = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,null=False,blank=False,primary_key=True,related_name="profile",related_query_name="profile")
    first_name = models.CharField(verbose_name=_('first name'),max_length=100,null=True,blank=True)
    last_name  = models.CharField(verbose_name=_('last name'),max_length=100,null=True,blank=True)
    address    = models.CharField(verbose_name=_('address'),blank=True,null=True,max_length=200)
    mobile     = models.CharField(verbose_name=_('mobile'), max_length=17,blank=True,null=True,unique=True)
    email      = models.EmailField(verbose_name=_('email'),null=False,blank=False,unique=True)
    branch     = models.CharField(verbose_name=_("branch"),null=True,blank=True,max_length=50)
    picture    = models.ImageField(upload_to=upload_user_data, null=True, blank=True, verbose_name=_(u"image"))

    class Meta:
        db_table = "users_profiles"
        
    
    def full_name(self):
        if(self.first_name == None):
            return self.user.get_username()
        return '{} {}'.format(self.first_name, self.last_name)


    def __str__(self):
        return '%s Profile' % self.user.username

 
