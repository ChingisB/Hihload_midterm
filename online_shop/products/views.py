from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Product, Inventory, Category
from .serializers import CategorySerializer, InventorySerializer, ProductSerializer


class CategoryListCreateView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        return super().get(request)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        return super().get(request)


class ProductListCreateView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        return super().get(request)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        return super().get(request)


# It's a custom view. So it's for retrieving specific products inventory
class ProductInventoryView(generics.RetrieveAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        return Inventory.objects.filter(product_id=self.kwargs['product_id'])

    def get_object(self):
        try:
            return self.get_queryset().get()
        except Inventory.DoesNotExist:
            return Response({"detail": "Inventory not found."}, status=status.HTTP_404_NOT_FOUND)
    
    @method_decorator(cache_page(60 * 5))
    def get(self, request):
        return super().get(request)