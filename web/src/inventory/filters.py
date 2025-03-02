import django_filters
from .models import Product, Model, Item, Location

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact','icontains'],
        }
