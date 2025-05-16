from rest_framework import serializers
from .models import Product, Category

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'stock', 'price', 'image', 'category', 'date_added']