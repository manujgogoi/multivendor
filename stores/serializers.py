from rest_framework import serializers
from stores.models import Category, Product, Specification, Image

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    
    products = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, many=True)

    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = Category
        fields = ['url', 'id', 'title', 'is_active', 'parent', 'products']


class SpecificationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Specification
        fields = ['id', 'url', 'name', 'value', 'url', 'product']

class ImageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = [ 'id', 'url', 'image', 'alt_text', 'is_featured', 'product']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    specifications = serializers.HyperlinkedIdentityField(view_name='specification-detail', many=True)
    images = serializers.HyperlinkedIdentityField(view_name='image-detail', read_only=True, many=True)
    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'description', 'sku', 'regular_price', 'discount_price', 'wholesale_price', 'quantity', 'wholesale_min_quantity', 'category', 'vendor', 'is_active', 'is_featured', 'is_downloadable', 'images', 'specifications']
        read_only_fields = ['vendor']
