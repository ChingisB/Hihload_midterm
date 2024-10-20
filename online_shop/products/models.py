from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(20)
    description = models.CharField(140)


class Product(models.Model):
    name = models.CharField(20)
    description = models.CharField(140)
    price = models.FloatField()
    categories = models.ManyToManyField("Category", related_name="categories", through="ProductCategory")

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["price"])
        ]


class Inventory(models.Model):
    count = models.IntegerField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)


class ProductCategory(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'product']),
            models.Index(fields=['category']),
        ]
        unique_together = ('category', 'product') 