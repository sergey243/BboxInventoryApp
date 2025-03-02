# Generated by Django 4.2.8 on 2025-03-01 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(editable=False, verbose_name="created on"),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        editable=False, verbose_name="last modified on"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="enter 500 characters description",
                        max_length=500,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "new"),
                            (1, "renovated"),
                            (2, "to renovate - repairable on site"),
                            (3, "to renovate - to transfer to the rc"),
                            (4, "to renovate - to scrap"),
                        ],
                        verbose_name="product status",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(default=0, verbose_name="available qunatity"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="item_creator",
                        related_query_name="item_creators",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modify_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="item_updater",
                        related_query_name="items_updater",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "items",
                "permissions": (
                    ("can_create_item", "can perform a new item"),
                    ("can_remove_item", "can cancel item"),
                    ("can_change_item", "can update a item"),
                    ("can_view_item", "can view item"),
                    ("can_approve_item", "can approve item"),
                ),
                "get_latest_by": ["location", "quantity"],
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(editable=False, verbose_name="created on"),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        editable=False, verbose_name="last modified on"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="name")),
                (
                    "address",
                    models.TextField(
                        blank=True, max_length=500, null=True, verbose_name="address"
                    ),
                ),
                (
                    "location_type",
                    models.CharField(
                        choices=[("dc", "dc"), ("shop", "shop"), ("client", "client")],
                        max_length=30,
                        verbose_name="location type",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="city",
                        to="cities_light.city",
                        verbose_name="city",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="country",
                        to="cities_light.country",
                        verbose_name="country",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="location_creator",
                        related_query_name="locations_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modify_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="location_updater",
                        related_query_name="locations_updaters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "locations",
                "permissions": (
                    ("can_create_location", "can perform a new location"),
                    ("can_remove_location", "can cancel location"),
                    ("can_change_location", "can update a location"),
                    ("can_view_location", "can view location"),
                    ("can_approve_location", "can approve location"),
                ),
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(editable=False, verbose_name="created on"),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        editable=False, verbose_name="last modified on"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="name")),
                (
                    "description",
                    models.CharField(max_length=30, verbose_name="description"),
                ),
                (
                    "min_required",
                    models.FloatField(
                        blank=True, verbose_name="minimum required in stock"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_creator",
                        related_query_name="products_creators",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "last_modify_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_updater",
                        related_query_name="products_updaters",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "products",
                "permissions": (
                    ("can_create_location", "can perform a new location"),
                    ("can_remove_location", "can cancel location"),
                    ("can_change_location", "can update a location"),
                    ("can_view_location", "can view location"),
                    ("can_approve_location", "can approve location"),
                ),
            },
        ),
        migrations.CreateModel(
            name="Movement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(editable=False, verbose_name="created on"),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        editable=False, verbose_name="last modified on"
                    ),
                ),
                (
                    "particular",
                    models.TextField(
                        blank=True,
                        help_text="enter 500 characters description",
                        max_length=500,
                        null=True,
                        verbose_name="movement particular",
                    ),
                ),
                (
                    "quantity",
                    models.IntegerField(default=0, verbose_name="available qunatity"),
                ),
                ("approved", models.BooleanField(default=False, verbose_name="status")),
                (
                    "approved_on",
                    models.DateTimeField(editable=False, verbose_name="approved on"),
                ),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movement_approved",
                        related_query_name="movements_approved",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movement_created",
                        related_query_name="movements_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movement_destination",
                        related_query_name="movements_destinations",
                        to="inventory.location",
                        verbose_name="destination",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="moved_item",
                        related_query_name="moved_items",
                        to="inventory.item",
                        verbose_name="item",
                    ),
                ),
                (
                    "last_modify_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movement_updated",
                        related_query_name="movements_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "received_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movement_received",
                        related_query_name="movements_received",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="movement_sources",
                        related_query_name="movements_source",
                        to="inventory.location",
                        verbose_name="source",
                    ),
                ),
            ],
            options={
                "db_table": "movements",
                "permissions": (
                    ("can_create_movement", "can perform a new movement"),
                    ("can_remove_movement", "can remove movement"),
                    ("can_change_movement", "can update a movement"),
                    ("can_view_movement", "can view movements"),
                    ("can_approve_movement", "can approve movements"),
                    ("can_receive_movement", "can acknoledge receipt on movements"),
                ),
                "get_latest_by": ["-created_on"],
            },
        ),
        migrations.AddField(
            model_name="item",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="item",
                related_query_name="items",
                to="inventory.location",
                verbose_name="location",
            ),
        ),
        migrations.AddField(
            model_name="item",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="item",
                related_query_name="items",
                to="inventory.product",
                verbose_name="category",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="item", unique_together={("location", "status", "product")},
        ),
    ]
