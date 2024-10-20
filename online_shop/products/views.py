from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Inventory, Category
from .serializers import CategorySerializer, InventorySerializer, ProductSerializer


class CategoryListCreateView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class =  CategorySerializer


class ProductListCreateView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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