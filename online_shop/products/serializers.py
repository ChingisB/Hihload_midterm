# serializers.py

from rest_framework import serializers
from .models import Category, Product, Inventory, ProductCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = ProductCategory
        fields = ['id', 'category', 'category_id']


class ProductSerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True
    )
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'categories', 'category_ids']

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        product = Product.objects.create(**validated_data)
        Inventory.objects.create(product=product, count=0)
        for category in category_ids:
            ProductCategory.objects.create(product=product, category=category)
        return product

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        instance.categories.clear()
        for category in category_ids:
            ProductCategory.objects.create(product=instance, category=category)

        return instance


class InventorySerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'count', 'product', 'product_id']
