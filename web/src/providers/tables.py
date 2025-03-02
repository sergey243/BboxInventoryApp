from django.utils.safestring import mark_safe
from django_tables2 import tables
from django.utils.translation import gettext_lazy as _
from django_tables2.utils import A
from .models import Provider, Service, Good, Work, Evaluation

class MaterializeCssCheckboxColumn(tables.columns.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.AttributeDict(default, **(specific or general or {}))
        return mark_safe("<p><label><input %s/><span></span></label></p>" % attrs.as_html())

class ProviderTable(tables.Table) :
    check = MaterializeCssCheckboxColumn(accessor='pk')
    created_at = tables.columns.DateColumn(accessor="created_at",verbose_name=_('Created at'),format='d/m/Y')
    creator = tables.columns.DateColumn(accessor="created_by__username",verbose_name=_('Created by'))
    designation = tables.columns.LinkColumn(accessor="designation",verbose_name=_('Designation'))
    city = tables.columns.Column(accessor="city.name",verbose_name=_('City'))
    is_service_provider = tables.columns.Column(verbose_name=_('Services'),orderable=False)
    is_contractor = tables.columns.Column(verbose_name=_('Contractor'),orderable=False)
    is_good_provider = tables.columns.Column(verbose_name=_('Goods'),orderable=False)
    class Meta:
        model = Provider
        template_name = "table.html"
        fields = ('check',"created_at","designation","city",'is_contractor',"is_service_provider","is_good_provider" )
    def render_creator(self, record):
        if(record.created_by):
            return record.created_by.username
        return ""
    def render_is_service_provider(self, record):
        return _('Yes') if record.is_service_provider else _('No')
    def render_is_contractor(self, record):
        return _('Yes') if record.is_contractor else _('No')
    def render_is_good_provider(self, record):
        return _('Yes') if record.is_good_provider else _('No')
    
class GoodsTable(tables.Table):
    check = MaterializeCssCheckboxColumn(accessor='pk')
    name = tables.columns.LinkColumn(accessor="name",verbose_name=_('Name'))
    description = tables.columns.Column(accessor="description",verbose_name=_('Description'),orderable=False)
    class Meta:
        model = Good
        template_name = "table.html"
        fields = ('check','name',"description" )
    

class WorksTable(tables.Table):
    check = MaterializeCssCheckboxColumn(accessor='pk')
    name = tables.columns.LinkColumn(accessor="name",verbose_name=_('Name'))
    description = tables.columns.Column(accessor="description",verbose_name=_('Description'),orderable=False)
    class Meta:
        model = Work
        template_name = "table.html"
        fields = ('check','name',"description" )

class ServicesTable(tables.Table):
    check = MaterializeCssCheckboxColumn(accessor='pk')
    name = tables.columns.LinkColumn(accessor="name",verbose_name=_('Name'))
    description = tables.columns.Column(accessor="description",verbose_name=_('Description'),orderable=False)
    class Meta:
        model = Service
        template_name = "table.html"
        fields = ('check','name',"description" )

class EvaluationTable(tables.Table):
    created_at = tables.columns.DateColumn(accessor="created_at",verbose_name=_('Created at'),format='d/m/Y')
    creator = tables.columns.DateColumn(accessor="created_by__username",verbose_name=_('Created by'))
    performance = tables.columns.Column(verbose_name=_('Performance'),orderable=True)
    po_number = tables.columns.LinkColumn('evaluation-update', args=[A('pk')], orderable=True)
    note = tables.columns.Column(verbose_name=_('Result'),orderable=True)
    def render_creator(self, record):
        if(record.created_by):
            return record.created_by.username
    def render_note(self, record):
        return record.note
    def render_performance(self, record):
        return record.performance
    class Meta:
        model = Evaluation
        template_name = "table.html"
        fields = ('created_at','po_number','period_start','period_end','lta','po_amount')