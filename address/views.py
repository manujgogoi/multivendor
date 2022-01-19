from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, mixins
from address.models import State, District, PIN, VillageOrTown
from address.serializers import StateSerializer, DistrictSerializer, PINSerializer, VillageOrTownSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class StateViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = State.objects.all()
    serializer_class = StateSerializer

    # Custom action to get districts of the current state
    @action(detail=True, methods=['get'])
    def districts(self, request, pk=None):
        queryset = District.objects.filter(state__id=pk)
        serializer = DistrictSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class DistrictViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    # Custom action to get pin codes of the current district
    @action(detail=True, methods=['get'])
    def pins(self, request, pk=None):
        queryset = PIN.objects.filter(district__id=pk)
        serializer = PINSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

class PINViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = PIN.objects.all()
    serializer_class = PINSerializer

    # Custom actin to get villages or towns of the current PIN
    @action(detail=True, methods=['get'])
    def villages_or_towns(self, request, pk=None):
        queryset = VillageOrTown.objects.filter(pin__id=pk)
        serializer = VillageOrTownSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class VillageOrTownViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = VillageOrTown.objects.all()
    serializer_class = VillageOrTownSerializer


# class AddressViewSet(mixins.CreateModelMixin, 
#                   mixins.RetrieveModelMixin, 
#                   mixins.DestroyModelMixin,
#                   mixins.ListModelMixin,
#                   viewsets.GenericViewSet):

#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer