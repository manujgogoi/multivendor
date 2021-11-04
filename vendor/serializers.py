from rest_framework import serializers
from vendor.models import Vendor
from accounts.views import User

class VendorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vendor
        fields = ['url', 'id', 'name', 'is_active', 'is_verified', 'created_at', 'owner']