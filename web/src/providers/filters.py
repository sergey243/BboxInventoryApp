from django import forms
import django_filters 
from django.utils.translation import gettext_lazy as _
from cities_light.models import City
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, MultiField, Row, Column
from django.db.models import Q
from .models import Provider, OFFERS, Service, Good, Work
from .forms import ProviderFilterForm

class ProviderFilter(django_filters.FilterSet):
    designation = django_filters.CharFilter(field_name='designation',lookup_expr='icontains',label=_('Designation'),
                                            widget=forms.widgets.TextInput(attrs={'placeholder': _('Designation should contain')}))
    cover = django_filters.MultipleChoiceFilter(label=_('Teritorial cover'),method='filter_cover')
    services = django_filters.ModelMultipleChoiceFilter(field_name='services',queryset=Service.objects.all())
    goods = django_filters.ModelMultipleChoiceFilter(field_name='goods',queryset=Good.objects.all())
    works = django_filters.ModelMultipleChoiceFilter(field_name='works',queryset=Work.objects.all())
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.filters['cover'].extra['choices'] = [(x.pk, x.name) for x in City.objects.all()]
        except (KeyError, AttributeError):
            pass
    def filter_cover(self, queryset, name, value):
        if(value):
            cities = City.objects.filter(pk__in=value)
            q = queryset.filter(Q(city__in=cities) | Q(covered_cities_Goods__in=cities) | Q(covered_cities_works__in=cities) | Q(covered_cities_services__in=cities)).distinct()
        return q
    
    class Meta:
        form = ProviderFilterForm
        model = Provider
        fields = {
            'designation',
        }

class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains',label=_('Name'),
                                            widget=forms.widgets.TextInput(attrs={'placeholder': _('Name should contain')}))
    
    class Meta:
        model = Service
        fields = {
            'name',
        }

class GoodFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains',label=_('Name'),
                                            widget=forms.widgets.TextInput(attrs={'placeholder': _('Name should contain')}))
    
    class Meta:
        model = Good
        fields = {
            'name',
        }

class WorkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains',label=_('Name'),
                                            widget=forms.widgets.TextInput(attrs={'placeholder': _('Name should contain')}))
    class Meta:
        model = Work
        fields = {
            'name',
        }


        