from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Item, Movement, Product, Location
from .serializers import LocationSerializer, ItemSerializer, MovementSerializer, ProductSerializer
from ..filters import ProductFilter

class ProdcutListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    

    def get(self, request):
        get_data = request.GET 
        articles = Product.objects.all()
        serializer = ProductSerializer(articles, many=True)

        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        pass

    def delete(self, request):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def patch(self, request, *args, **kwargs):
        pass
