from typing import Any
from  django import forms
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Provider, Service, Good, Work, Evaluation
from utils.fields import CommaSeparatedField

class ProviderFilterForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout =  Layout(
            Div(
                Div('designation', css_class='form-group col-md-12 mb-0'),
                css_class='form-row row g-4"'
            ),
            Div(
                Div('services', css_class='form-group col-md-4 mb-0'),
                Div('works', css_class='form-group col-md-4 mb-0'),
                Div('goods', css_class='form-group col-md-4 mb-0'),
                css_class='form-row row g-4"'
            ),
            Div(
                Div('cover', css_class='form-group col-md-12 mb-0'),
                css_class='form-row row g-4"'
            )

        )
        self.helper.add_input(Submit('submit', 'Submit'))
    


class ProviderForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(ProviderForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].widget.attrs['rows'] = 3
        self.fields['affiliations'].widget.attrs['rows'] = 3
        self.fields['equipments'].widget.attrs['rows'] = 3
        self.fields['subsidiaries'].widget.attrs['rows'] = 3
        self.fields['comment'].widget.attrs['rows'] = 3
        self.fields['competition'].widget.attrs['rows'] = 3
        self.fields['offers_previously_provided'].widget.attrs['rows'] = 3
        self.fields['address'].widget.attrs['rows'] = 3
    
    def clean_tax_id(self):
        tax_id = self.cleaned_data["tax_id"]
        queryset = Provider.objects.filter(tax_id=tax_id)
        if(queryset.exists() and tax_id != None):
            if(queryset.count() == 1 and queryset.first().pk == self.instance.pk ): pass
            else: 
                url = reverse_lazy('provider-details', args=[queryset.first().pk])
                link_text = _("see provider")
                link = '<a target="_blank" href="{}">{}</a>'.format(url,link_text)
                error_text = _('Provider with same tax identification number exist')
                raise ValidationError(format_html('{} ({}).'.format(error_text,link)))
        return tax_id
    
    def clean_ungm_number(self):
        ungm_number = self.cleaned_data["ungm_number"]
        queryset = Provider.objects.filter(ungm_number=ungm_number)
        if(queryset.exists() and ungm_number != None):
            if(queryset.count() == 1 and queryset.first().pk == self.instance.pk ): pass
            else: 
                url = reverse_lazy('provider-details', args=[queryset.first().pk])
                link_text = _("see provider")
                link = '<a target="_blank" href="{}">{}</a>'.format(url,link_text)
                error_text = _('Provider with same UNGM number exist')
                raise ValidationError(format_html('{} ({}).'.format(error_text,link)))
        return ungm_number
    
    def clean_unicef_vendor_number(self):
        unicef_vendor_number = self.cleaned_data["unicef_vendor_number"]
        queryset = Provider.objects.filter(unicef_vendor_number=unicef_vendor_number)
        if(queryset.exists() and unicef_vendor_number != None):
            if(queryset.count() == 1 and queryset.first().pk == self.instance.pk ): pass
            else:
                url = reverse_lazy('provider-details', args=[queryset.first().pk])
                link_text = _("see provider")
                link = '<a target="_blank" href="{}">{}</a>'.format(url,link_text)
                error_text = _('Provider with same Unicef vendor number exist')
                raise ValidationError(format_html('{} ({}).'.format(error_text,link)))

        return unicef_vendor_number
    def clean_covered_cities_Goods(self):
        covered_cities_Goods = self.cleaned_data["covered_cities_Goods"]
        goods = self.cleaned_data["goods"]
        if(covered_cities_Goods.exists() and not goods.exists()):
            raise ValidationError(_('No good had been selected, please select the goods provided in the field Goods provided.'))
        if(not covered_cities_Goods.exists() and goods.exists()):
            raise ValidationError(_('No city had been selected for goods, please select the city/cities where googs are provided.'))
        return covered_cities_Goods

   
    def clean_covered_cities_works(self):
        covered_cities_works = self.cleaned_data["covered_cities_works"]
        works = self.cleaned_data["works"]
        if(covered_cities_works.exists() and not works.exists()):
            raise ValidationError(_('No work had been selected, please select the work provided in the field works provided.'))
        if(not covered_cities_works.exists() and works.exists()):
            raise ValidationError(_('No city had been selected for work, please select the city/cities where works are provided.'))
        return covered_cities_works

    def clean_covered_cities_services(self):
        covered_cities_services = self.cleaned_data["covered_cities_services"]
        services = self.cleaned_data["services"]
        if(covered_cities_services.exists() and not services.exists()):
            raise ValidationError(_('No service had been selected, please select the services provided in the field Services provided.'))
        if(not covered_cities_services.exists() and services.exists()):
            raise ValidationError(_('No city had been selected for services, please select the city/cities where services are provided'))
        return covered_cities_services

    class Meta:
        model = Provider
        fields = ("designation", "responsible", "contacts", "phone",
                    "email","website",'city','address','works','goods','services',
                    'subsidiaries','tax_id','rccm','national_id','bank_domiciliation',
                    'active_since','ungm_number','unicef_vendor_number',
                    'is_manifactor','is_importer','goods_orgin','is_retailer','is_wholeseller',
                    'annual_turnover_crncy','last_turnover','past_annual_turnover',
                    'employees_count','is_accredited_provider','partners',
                    'workspaces','equipments','competition','affiliations','affiliate_to_commerce_chamber',
                    'reason_no_affiliate','offers_previously_provided','selection_mode',
                    'advantages','covered_cities_Goods','covered_cities_works',
                    'covered_cities_services','comment')
        
class BulkDeleteForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    selection = CommaSeparatedField()
        
class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 5
    class Meta:
        model = Service
        fields = ("name", "description")

class GoodForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(GoodForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 5
    class Meta:
        model = Good
        fields = ("name", "description")

class WorkForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs['rows'] = 5
    class Meta:
        model = Work
        fields = ("name", "description")

class EvaluationForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    def __init__(self, *args, **kwargs):
        super(EvaluationForm, self).__init__(*args, **kwargs)
        self.fields['provider'].widget.attrs['disabled'] = 'disabled'
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['comment'].widget.attrs['rows'] = 5
        self.fields['period_start'].widget = DatePickerInput()
        self.fields['period_end'].widget = DatePickerInput()

    def clean(self) -> "dict[str, Any]":
        clean_data = super().clean()
        site = clean_data.get("site")
        provider = clean_data.get("provider")
        period_start = clean_data.get("period_start")
        period_end = clean_data.get("period_end") 
        if(period_start == None or period_end == None):
            return clean_data
        if(self.instance):
            queryset = Evaluation.objects.filter(~Q(pk=self.instance.pk),provider=provider,site=site)
            
            if queryset.filter(period_start__gte=period_start, period_end__lte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
            elif queryset.filter(Q(period_start__lt=period_start) & Q(period_start__lt=period_end), period_end__lte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
            elif queryset.filter(Q(period_start__gte=period_start) & Q(period_start__lt=period_end),period_end__gte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
            elif queryset.filter(period_start__lte=period_start, period_end__gte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
        else:
            queryset = Evaluation.objects.filter(provider=provider,site=site)
            if queryset.filter(period_start__gte=period_start, period_end__lte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
            elif queryset.filter(Q(period_start__lt=period_start) & Q(period_start__lt=period_end), period_end__lte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
            elif queryset.filter(Q(period_start__gte=period_start) & Q(period_start__lt=period_end),period_end__gte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
            elif queryset.filter(period_start__lte=period_start, period_end__gte=period_end).exists():
                raise ValidationError(_('Evaluation timing confict with another evalution.'))
        return clean_data
    
    def clean_provider(self):
        return self.cleaned_data["provider"]
        

    def clean_period_end(self):
        period_end = self.cleaned_data["period_end"]
        period_start = self.cleaned_data["period_start"]
        if(period_end != None and period_start != None):
            if period_end <= period_start:
                raise ValidationError(_('Period start cannot be greater or equal to period end'))
            

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return period_end
    class Meta:
        model = Evaluation
        fields = ("provider","site","services","works","goods","period_start","period_end","lta","po_number","po_amount","description",
                    "fiability","timing","best_value","tech_specification","conclusion","comment")

        