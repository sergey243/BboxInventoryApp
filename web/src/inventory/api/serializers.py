from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from ..models import Item, Location, Movement, Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on', 'created_by', 'last_modify_by')


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('created_on', 'modified_on', 'created_by', 'last_modify_by','name','country','city','location_type','address')
        read_only_fields = ('created_on', 'modified_on', 'created_by', 'last_modify_by')


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on', 'created_by', 'last_modify_by')

class MovementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movement
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on', 'created_by', 'last_modify_by')