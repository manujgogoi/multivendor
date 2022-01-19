from django.contrib.auth import get_user_model
from rest_framework import serializers
from address.models import State, District, PIN, VillageOrTown

User = get_user_model()

class StateSerializer(serializers.HyperlinkedModelSerializer):

    districts = serializers.HyperlinkedRelatedField(view_name='district-detail', read_only=True, many=True)

    class Meta:
        model = State
        fields = ['url', 'id', 'name', 'is_deliverable', 'districts']


class DistrictSerializer(serializers.HyperlinkedModelSerializer):

    pin_codes = serializers.HyperlinkedRelatedField(view_name="pin-detail", read_only=True, many=True)

    class Meta:
        model = District
        fields = ['url', 'id', 'name', 'is_deliverable', 'pin_codes', 'state']

class PINSerializer(serializers.HyperlinkedModelSerializer):

    villages_or_towns = serializers.HyperlinkedRelatedField(view_name='villageortown-detail', read_only=True, many=True)

    class Meta:
        model = PIN
        fields = ['url', 'id', 'code', 'is_deliverable', 'villages_or_towns', 'district']


class VillageOrTownSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VillageOrTown
        fields = ['url', 'id', 'name', 'is_deliverable', 'pin']