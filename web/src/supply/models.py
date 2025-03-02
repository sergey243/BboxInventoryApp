from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class EntryPoint(models.Model):
    name = models.CharField(verbose_name=_("entry point"),blank=False,null=False,unique=True)

    class Meta:
        db_table = "entry_points"

class Order(models.Model):
    created_at = models.DateTimeField(editable=False,verbose_name=_("created at"))
    modified_at = models.DateTimeField(editable=False,verbose_name=_("last modified at"))
    created_by = models.ManyToOneRel(get_user_model(), on_delete=models.PROTECT,null=False,blank=False,primary_key=True,related_name="orders",related_query_name="order")
    #entry_point = 
    class Meta:
        db_table = "orders"
        get_latest_by = ["-priority", "order_date"]
