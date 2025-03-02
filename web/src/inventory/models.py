from django.db import models
from django.db.models import fields, Model, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from cities_light import models as cities_models
from django.contrib.auth import get_user_model


class Product(models.Model):
    """
    A class representing a type of product.

    Attributes:
        created_on (datetime): The creation date.
        modified_on (datetime): The last modification date.
        created_by (user): The creator of the record.
        last_modify_by (user): The user who last modified the record.
        name (str): The name of the product.
        description (str): The description of the product.
        min_required (int): The minimum quantity required in stock before notification.
    """
    created_on = models.DateTimeField(editable=False,verbose_name=_("created on"))
    modified_on = models.DateTimeField(editable=False,verbose_name=_("last modified on"))
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,null=False,blank=False,related_name="product_creator",     related_query_name="products_creators")
    last_modify_by = models.ForeignKey(get_user_model(),editable=False,related_name="product_updater",related_query_name="products_updaters",null=True,blank=True,on_delete=models.PROTECT)
    name = models.fields.CharField(verbose_name=_("name"),max_length=30,blank=False,null=False)
    description = models.fields.CharField(verbose_name=_("description"),max_length=30,blank=False,null=False)
    min_required = models.fields.FloatField(verbose_name=_("minimum required in stock"),blank=True,null=False)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        if not self.created_on:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super(Product,self).save(*args,**kwargs)

    class Meta:
        permissions = (("can_create_location", _("can perform a new location")),
                       ("can_remove_location", _("can cancel location")),
                       ("can_change_location", _("can update a location")),
                       ("can_view_location", _("can view location")),
                       ("can_approve_location", _("can approve location")))          
        db_table = "products"

PRODUCT_STATUS = ((0,_(u'new')),(1,_(u'renovated')),(2,_(u'to renovate - repairable on site')),(3,_(u'to renovate - to transfer to the rc')),
                  (4,_(u'to renovate - to scrap')))

LOCATION_TYPES = (('dc',_(u'dc')),('shop',_(u'shop')),('client',_(u'client')))
class Location(models.Model):
    """
    A class representing a type of loction.
    Example: Shop, warehouse

    Attributes:
        created_on (datetime): The creation date.
        modified_on (datetime): The last modification date.
        created_by (user): The creator of the record.
        last_modify_by (user): The user who last modified the record.
        name (str): The name of the location.
        city (City): The city where the facility or client is located.
        location_type (str): The type of location.
    """
    created_on = models.DateTimeField(editable=False,verbose_name=_("created on"))
    modified_on = models.DateTimeField(editable=False,verbose_name=_("last modified on"))
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,null=False,blank=False,related_name="location_creator",related_query_name="locations_created")
    last_modify_by = models.ForeignKey(get_user_model(),editable=False,related_name="location_updater",related_query_name="locations_updaters",null=True,blank=True,on_delete=models.PROTECT)
    name = models.fields.CharField(verbose_name=_("name"),max_length=30,blank=False,null=False)
    country = models.ForeignKey('cities_light.Country',verbose_name= _('country'),on_delete=models.SET_NULL, null=True, blank=True,related_name="country") 
    city = models.ForeignKey(cities_models.City, related_name="city",verbose_name=_('city'),blank=True,null=True, on_delete=models.PROTECT)
    address = fields.TextField(verbose_name=_("address"),max_length=500,null=True,blank=True)
    location_type = models.CharField(verbose_name=_("location type"),max_length=30,blank=False,null=False,choices=LOCATION_TYPES)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        if not self.created_on:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super(Location,self).save(*args,**kwargs)
    
    class Meta:
        permissions = (("can_create_location", _("can perform a new location")),
                       ("can_remove_location", _("can cancel location")),
                       ("can_change_location", _("can update a location")),
                       ("can_view_location", _("can view location")),
                       ("can_approve_location", _("can approve location"))
                    )    
        db_table = "locations"

class Item(models.Model):
    """
    A class representing a products in a specific state.
    Example: new products, repossess product, renewed products

    Attributes:
        created_on (datetime): The creation date.
        modified_on (datetime): The last modification date.
        created_by (user): The creator of the record.
        last_modify_by (user): The user who last modified the record.
        description (str): The description of the item.
        status (str): The status of the item.
        product (Product): The related product.
        quantity (Product): The quantity in stock.
        location (Location): The location of the items.
    """
    created_on = models.DateTimeField(editable=False,verbose_name=_("created on"))
    modified_on = models.DateTimeField(editable=False,verbose_name=_("last modified on"))
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,null=False,blank=False,related_name="item_creator",related_query_name="item_creators")
    last_modify_by = models.ForeignKey(get_user_model(),editable=False,related_name="item_updater",related_query_name="items_updater",null=True,blank=True,on_delete=models.PROTECT)
    description = models.fields.TextField(verbose_name=_(u"description"),max_length=500,blank=True,null=True,help_text=_(u'enter 500 characters description'))
    status = models.fields.IntegerField(verbose_name=_(u'product status'),null=False,blank=False,choices=PRODUCT_STATUS)
    quantity = models.fields.IntegerField(verbose_name=_(u'available qunatity'),default=0,null=False,blank=False)
    product = models.ForeignKey("Product",verbose_name=_(u'category'),on_delete=models.PROTECT,related_query_name="items",related_name="item")
    location = models.ForeignKey("Location",verbose_name=_(u'location'),on_delete=models.PROTECT,related_query_name="items",related_name="item")

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        if not self.created_on:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super(Item,self).save(*args,**kwargs)
    class Meta:
        permissions = (("can_create_item", _("can perform a new item")),
                       ("can_remove_item", _("can cancel item")),
                       ("can_change_item", _("can update a item")),
                       ("can_view_item", _("can view item")),
                       ("can_approve_item", _("can approve item"))
                    )
        db_table = "items"
        unique_together = ('location', 'status','product')
        get_latest_by = ["location", "quantity"]
    
    
    #def get_absolute_url(self):
    #    return reverse('work-details',args=[self.pk])   
 
class Movement(models.Model):
    """
    A class representing a movement of items from one location to another.

    Attributes:
        created_on (datetime): The creation date.
        modified_on (datetime): The last modification date.
        created_by (user): The creator of the record.
        last_modify_by (user): The user who last modified the record.
        particular (str): The description of the movement.
        source (Location): The source location.
        destination (Location): The destination location.
        quantity (int): The quantity to move.
        item (Item): The related item.
        approved (Boolean): The validation status.
        approved_by (user): The validator.
        approved_on (DateTime): The validation date.
        received_by (user): The person wo received the items.
    """
    created_on = models.DateTimeField(editable=False,verbose_name=_("created on"))
    modified_on = models.DateTimeField(editable=False,verbose_name=_("last modified on"))
    created_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,null=False,blank=False,related_name="movement_created",related_query_name="movements_created")
    last_modify_by = models.ForeignKey(get_user_model(),editable=False,related_name="movement_updated",related_query_name="movements_updated",null=True,blank=True,on_delete=models.PROTECT)
    particular = models.fields.TextField(verbose_name=_(u"movement particular"),max_length=500,blank=True,null=True,help_text=_(u'enter 500 characters description'))
    source = models.ForeignKey("Location",verbose_name=_(u'source'),on_delete=models.PROTECT,related_query_name="movements_source",related_name="movement_sources")
    destination = models.ForeignKey("Location",verbose_name=_(u'destination'),on_delete=models.PROTECT,related_query_name="movements_destinations",related_name="movement_destination")
    quantity = models.fields.IntegerField(verbose_name=_(u'available qunatity'),default=0,null=False,blank=False)
    item =  models.ForeignKey("Item",verbose_name=_(u'item'),on_delete=models.CASCADE,related_query_name="moved_items",related_name="moved_item")
    approved =  models.fields.BooleanField(verbose_name=_(u'status'),default=False,blank=False,null=False)
    approved_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,null=True,blank=True,related_name="movement_approved",related_query_name="movements_approved")
    approved_on = models.DateTimeField(editable=False,verbose_name=_("approved on"))
    received_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,null=True,blank=True,related_name="movement_received",related_query_name="movements_received")
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
            self.approved = False
        if not self.created_on:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super(Item,self).save(*args,**kwargs)
    
    def approve(self, *args, **kwargs):
        pass

    def acknoledge_receipt(self, *args, **kwargs):
        pass
    
    class Meta:
        db_table = "movements"
        get_latest_by = ["-created_on"]
        permissions = (("can_create_movement", _("can perform a new movement")),
                       ("can_remove_movement", _("can remove movement")),
                       ("can_change_movement", _("can update a movement")),
                       ("can_view_movement", _("can view movements")),
                       ("can_approve_movement", _("can approve movements")),
                       ("can_receive_movement", _("can acknoledge receipt on movements")),
                    )