from django.core.exceptions import ObjectDoesNotExist
from django_filters.utils import translate_validation
from rest_framework.pagination import PageNumberPagination
from .models import Item, Location, Product, Movement
from .filters import ProductFilter


class ProductService:
    @staticmethod
    def get_product_by_id(id:int) -> Product:
        '''
        Return the product that matches the provided id
            Parameters:
                    id (int): The product id
            Returns:
                    product (Product): matching product
        '''
        return Product.objects.filter(pk=id).first()
    
    @staticmethod
    def find_products(params):
        '''
        Return the product that matches the provided id
            Parameters:
                    id (int): The product id
            Returns:
                    product (django.db.models.QuerySet): matching products
        '''
        filterset = ProductFilter(params, queryset=Product.objects.all())
        if not filterset.is_valid():
            raise translate_validation(filterset.errors)
        return filterset.qs

    @staticmethod
    def delete_product():
        pass

    @staticmethod
    def create_product(**kwargs):
        pass

    @staticmethod
    def delete_product(id:int) -> tuple[int,dict[str, int]]:
        '''
        Return the number of product deleted
        Raise a ObjectDoesNotExist exception if the entry does not exist
            Parameters:
                    id (int): The product id
            Returns:
                    deleted (tuple[int,dict[str, int]]): number of deleted items with list deleted ids
        '''
        products = Product.objects.filter(pk=id)
        if not products.exists: raise ObjectDoesNotExist()
        return products.first().delete()
    
    @staticmethod
    def delete_products(params) -> tuple[int,dict[str, int]]:
        '''
        Return the number of product deleted
        Raise a ObjectDoesNotExist exception if the entry does not exist
            Parameters:
                    params (django.http.QueryDict): request params
            Returns:
                    deleted (tuple[int,dict[str, int]]): number of deleted items with list deleted ids
        '''
        filterset = ProductFilter(params, queryset=Product.objects.all())
        if not filterset.is_valid():
            raise translate_validation(filterset.errors)
        return filterset.qs.delete()

class LocationService:
    @staticmethod
    def get_locaion_by_id():
        pass
    @staticmethod
    def find_locations():
        pass
    @staticmethod
    def delete_location():
        pass
    @staticmethod
    def create_location():
        pass
    @staticmethod
    def delete_location():
        pass
    @staticmethod
    def delete_locations():
        pass

class ItemService:
    @staticmethod
    def get_item_by_id():
        pass
    @staticmethod
    def find_items():
        pass
    @staticmethod
    def delete_item():
        pass
    @staticmethod
    def create_item():
        pass
    @staticmethod
    def delete_item():
        pass
    @staticmethod
    def delete_items():
        pass
    @staticmethod
    def delete_itemss():
        pass
    @staticmethod
    def move_itemss():
        pass

class MovementService():
    pass