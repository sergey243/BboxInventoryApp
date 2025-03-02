from django.db import models
from django.db.models import fields, Model, Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy,reverse
from django.utils.html import mark_safe, format_html
from cities_light import models as cities_models
from multiselectfield import MultiSelectField
from django.urls import reverse

CURRENCIES = (
    ('USD',_('US Dollars')),
    ('CDF',_('Congolese franc')),
    ('CFA',_('Central African CFA franc')),
    ('TZS',_('Tanzanian shilling')),
    ('AOA',_('Angolan kwanza')),
    ('UGX',_('Ugandan Shillings')),
    ('BIF',_('Burundian franc')),
    ('ZMW',_('Congolese franc')),
    ('CDF',_('Zambian kwacha')),
)

SELECTION_MODE = (
    ('tender',_('On tender call')),
    ('consultation',_('Restricted consultation')),
    ('exclusive',_('On direct order'))
)

ADVANTAGES = (
    ('after sales service',_('After sales service')),
    ('discounts/rebates',_('Discounts/rebates')),
    ('on-site deliveries',_('On-site deliveries'))
)

EVALUATION = (
    (1,_('poor')),
    (2,_('not satisfying')),
    (3,_('acceptable')),
    (4,_('good')),
    (5,_('excelent'))
)

EVALUATION_CONCLUSION = (
    (0, _("Yes, we can keep working with this provider.")),
    (1, _("No, we should not be working with this provider anymore."))
)


class Provider(Model):
    created_at = fields.DateTimeField(editable=False,verbose_name=_("created at"))
    modified_at = fields.DateTimeField(editable=False,verbose_name=_("last modified at"))
    created_by = models.ForeignKey(get_user_model(),editable=False,related_name="pcreator",null=True,blank=True,on_delete=models.PROTECT)
    last_modify_by = models.ForeignKey(get_user_model(),editable=False,related_name="pmodifier",null=True,blank=True,on_delete=models.PROTECT)
    name = fields.CharField(verbose_name=_("name"),unique=True,max_length=250,null=False,blank=False)
    responsible = fields.CharField(verbose_name=_("responsible"),max_length=250,null=False,blank=False)
    contacts = fields.TextField(verbose_name=_("contacts"),max_length=500,null=True,blank=True)
    phone = fields.CharField(verbose_name=_("phone"),max_length=150,null=True,blank=True)
    email = fields.EmailField(verbose_name=_("email"),max_length=150,null=True,blank=True)
    website = fields.CharField(verbose_name=_("website"),max_length=500,null=True,blank=True)
    country = models.ForeignKey('cities_light.Country',verbose_name= _('country'),on_delete=models.SET_NULL, null=True, blank=True,related_name="country") 
    city = models.ForeignKey('cities_light.City',verbose_name= _('city'), on_delete=models.SET_NULL, null=True, blank=True)
    address = fields.TextField(verbose_name=_("address"),max_length=500,null=True,blank=True)
    vendor_id = fields.CharField(verbose_name=_("vendo ID"),max_length=150, blank=True, null=True)
    advantages = MultiSelectField(verbose_name=_("proposed advantages"),choices=ADVANTAGES, blank=True, null=True,max_choices=3, max_length=2048)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        queryset = Provider.objects.filter(unicef_vendor_number= self.unicef_vendor_number)
        if queryset.exists() and self.vendor_id != None:
            if(queryset.count() == 1 and queryset.first().pk == self.pk ): pass
            else:
                url = reverse_lazy('provider-details', args=[queryset.first().pk])
                link_text = _("see provider")
                link = '<a target="_blank" href="{}">{}</a>'.format(url,link_text)
                error_text = _('Provider with same  vendor ID exist')
                raise ValidationError(format_html('{} ({}).'.format(error_text,link)))

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        if not self.created_at:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Provider,self).save(*args,**kwargs)

    def __str__(self):
        return self.designation

    def get_absolute_url(self):
        return reverse('provider-details',args=[self.pk])
    class Meta:
        permissions = (("can_create_provider", _("can create a new provider")),
                       ("can_remove_provider", _("can remove provider")),
                       ("can_change_provider", _("can update a provider")),
                       ("can_visualize_provider", _("can visualize provider")),
                    )
        db_table_comment = "Provider identified and retained by Unicef"
        default_related_name = "providers"
        get_latest_by = ["created_at","modified_at"]
        get_latest_by = ["created_at","modified_at"]
        ordering = ["designation"]
        db_table = "providers"

class Evaluation(Model):
    created_at = fields.DateTimeField(editable=False,verbose_name=_("created at"))
    modified_at = fields.DateTimeField(editable=False,verbose_name=_("last modified at"))
    created_by = models.ForeignKey(get_user_model(),editable=False,related_name="ecreator",null=True,blank=True,on_delete=models.PROTECT)
    last_modify_by = models.ForeignKey(get_user_model(),editable=False,related_name="emodifier",null=True,blank=True,on_delete=models.PROTECT)
    provider = models.ForeignKey('Provider',related_name="provider", on_delete=models.CASCADE, verbose_name=_('provider'))
    period_start = models.DateField(verbose_name=_('period start'),blank=False,null=False)
    period_end = models.DateField(verbose_name=_('period end'),blank=False,null=False)
    lta = models.CharField(verbose_name=_('LTA number'),max_length=50,blank=False,null=False)
    po_number = models.CharField(verbose_name=_('PO number'),max_length=50,blank=False,null=False)
    po_amount = models.DecimalField(verbose_name=_('PO amount'),decimal_places=2,max_digits=20,blank=False,null=False)
    description = fields.TextField(verbose_name=_("description"),max_length=500,null=True,blank=True)
    fiability = fields.IntegerField(verbose_name=_('fiability'),choices=EVALUATION,blank=False, null=False,help_text=_('Note on the scale from 1 to 5'))
    timing = fields.IntegerField(verbose_name=_('timing'),choices=EVALUATION,blank=False, null=False,help_text=_('Note on the scale from 1 to 5'))
    best_value = fields.IntegerField(verbose_name=_('quality-price report'),choices=EVALUATION,blank=False, null=False,help_text=_('Note on the scale from 1 to 5'))
    tech_specification = fields.IntegerField(verbose_name=_('technical specifications'),choices=EVALUATION,blank=False, null=False,help_text=_('Note on the scale from 1 to 5'))
    conclusion = models.IntegerField(verbose_name=_("conclusion"),choices=EVALUATION_CONCLUSION,blank=False,null=False)
    comment = fields.TextField(verbose_name=_("comment"),max_length=500,null=True,blank=True)

    @property
    def performance(self):
        _performance = self.fiability + self.timing + self.best_value + self.tech_specification
        if(_performance > 14): return 'A'
        elif(_performance <= 14 and _performance >= 10): return 'B'
        elif(_performance < 10 and _performance >= 3): return 'C'
        else: return 'D'
    @property
    def note(self):
        return self.fiability + self.best_value + self.tech_specification + self.timing
    
    def __str__(self):
        return '{}:'.format(self.pk)

    def save(self, *args, **kwargs):
        
        if not self.id:
            self.created_at = timezone.now()
        if not self.created_at:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        
        return super(Evaluation,self).save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('provider-details',args=[self.provider.pk])
    class Meta:
        permissions = (("can_create_evaluation", _("can create a new evaluation")),
                       ("can_remove_evaluation", _("can remove evaluation")),
                       ("can_change_evaluation", _("can update an evaluation")),
                       ("can_visualize_evaluation", _("can visualize evaluation")),
                    )
        default_related_name = "evaluations"
        get_latest_by = ["created_at","modified_at"]
        get_latest_by = ["created_at","modified_at"]
        ordering = ["provider"]
        db_table = "evaluations"
