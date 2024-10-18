# admin.py

from django.contrib import admin
from .models import Product, Category, Inventory, ProductCategory


class ProductCategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1


class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0
    readonly_fields = ['count']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']
    search_fields = ['name', 'description']
    inlines = [ProductCategoryInline, InventoryInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'count']
    search_fields = ['product__name']
    readonly_fields = ['product']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'category']
    search_fields = ['product__name', 'category__name']
