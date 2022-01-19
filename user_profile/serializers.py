from django.contrib.auth import get_user_model
from rest_framework import serializers
from user_profile.models import Profile, DeliveryAddress

User = get_user_model()

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', many=False, read_only=True)
    delivery_addresses = serializers.HyperlinkedRelatedField(view_name='deliveryaddress-detail', read_only=True, many=True)
    class Meta:
        model = Profile
        fields = [
            'url', 
            'id', 
            'first_name', 
            'middle_name', 
            'last_name', 
            'birthday', 
            'phone_number', 
            'is_phone_verified', 
            'photo', 
            'house_no', 
            'landmark', 
            'state', 
            'district', 
            'pin_code', 
            'village_or_town', 
            'delivery_addresses', 
            'user', 
            'created_at', 
            'updated_at'
        ]


class DeliveryAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DeliveryAddress
        fields = [
            'url', 
            'id', 
            'profile', 
            'state', 
            'district', 
            'pin_code', 
            'village_or_town', 
            'house_no', 
            'landmark', 
            'created_at', 
            'updated_at'
        ]