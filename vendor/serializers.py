from rest_framework import serializers
from django.contrib.auth import get_user_model
from vendor.models import Vendor
from stores.serializers import ProductSerializer

User = get_user_model()

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, many=True)
    # products = ProductSerializer(many=True)
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', many=False, read_only=True)
    class Meta:
        model = Vendor
        fields = ['url', 'id', 'name', 'is_active', 'is_verified', 'created_at', 'owner', 'products']
        read_only_fields = ['is_active', 'is_verified', 'owner']