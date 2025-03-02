from django.contrib import admin
from .models import Product, Location, Movement, Item
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","description","min_required")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

admin.site.register(Product,ProductAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ("name","country","city","location_type")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

admin.site.register(Location,LocationAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ("status","quantity","product","location")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

admin.site.register(Item,ItemAdmin)

class MovementAdmin(admin.ModelAdmin):
    list_display = ("created_on","source","destination","quantity","item","approved","approved_by","approved_on","received_by")
    list_per_page = 10
    def save_model(self, request, obj, form, change): 
        if obj.pk: 
            obj.created_by = request.user
        obj.last_modify_by = request.user
        obj.save()

admin.site.register(Movement,MovementAdmin)