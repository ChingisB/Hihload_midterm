from rest_framework import generics, status
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .models import Product, Inventory, Category
from .serializers import CategorySerializer, InventorySerializer, ProductSerializer
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoryListCreateView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(
            cache_page(60 * 5),
            swagger_auto_schema(
                responses={'200': 'ok'},
                name='category_list'
            )
    )
    def get(self, request):
        return super().get(request)


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(
            cache_page(60 * 5),
            swagger_auto_schema(
                manual_parameters=[
                    openapi.Parameter(name='pk', in_=openapi.IN_PATH, type='int', description='ID of category')
                ], 
                responses={'200': 'ok'},
                name='category detail'
            )
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductListCreateView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(
            cache_page(60 * 5),
            swagger_auto_schema(
                responses={'200': 'ok'},
                name='product list'
            )
    )
    def get(self, request):
        return super().get(request)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(
            cache_page(60 * 5),
            swagger_auto_schema(
                manual_parameters=[
                    openapi.Parameter(name='pk', in_=openapi.IN_PATH, type='int', description='ID of product')
                ], 
                responses={'200': 'ok'},
                name='product detail'
            ),         
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# It's a custom view. So it's for retrieving specific products inventory
class ProductInventoryView(generics.RetrieveAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        return Inventory.objects.filter(product_id=self.kwargs['pk'])

    def get_object(self):
        try:
            return self.get_queryset().get()
        except Inventory.DoesNotExist:
            raise Http404("Inventory not found.")
            
    @method_decorator(
            cache_page(60 * 5),
            swagger_auto_schema(
                manual_parameters=[
                    openapi.Parameter(name='pk', in_=openapi.IN_PATH, type='int', description='ID of product')
                ], 
                responses={'200': 'ok'},
                name='list'
            ), 
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)