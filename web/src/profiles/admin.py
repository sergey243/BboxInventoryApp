from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    #list_filter = ('rooms','tank', 'generator','parking','city')
    list_display = (
        'full_name',
        'mobile','email',)
    list_display_links = ('email',)
    def full_name(self,obj):
        return "%s %s" % (obj.first_name, obj.last_name)
