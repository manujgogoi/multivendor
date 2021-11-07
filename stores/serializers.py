from rest_framework import serializers
from stores.models import Category, Product, Specification, Image

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = Category
        fields = ['url', 'id', 'title', 'is_active', 'parent']


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'description', 'sku', 'regular_price', 'discount_price', 'wholesale_price', 'quantity', 'wholesale_min_quantity', 'category', 'vendor', 'is_active', 'is_featured', 'is_downloadable']


class SpecificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Specification

class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image