from django.contrib import admin
from providers.models import Service,Good,Work,Provider, Site
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
# Register your models here.

class SiteAdmin(admin.ModelAdmin):
    list_display = ("name","description")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name","description")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("name","description")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

class WorkAdmin(admin.ModelAdmin):
    list_display = ("name","description")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

class ServicesInline(admin.TabularInline):
    model = Provider.services.through

class GoodsInline(admin.TabularInline):
    model = Provider.goods.through

class WorksInline(admin.TabularInline):
    model = Provider.works.through

class ProviderAdmin(admin.ModelAdmin):
    inlines =[ServicesInline, GoodsInline, WorksInline]
    list_display = ("designation","city", "responsible",'phone','email','rccm','national_id','is_service_provider','is_contractor','is_good_provider')
    search_fields =('designation',)
    list_filter = (
        ('city', RelatedDropdownFilter),
    )
    list_per_page = 10 
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

admin.site.register(Service, ServiceAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Good, GoodsAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Site, SiteAdmin)

class ProviderAdmin(admin.ModelAdmin):
    pass