from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, mixins, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from user_profile.models import Profile, DeliveryAddress
from user_profile.serializers import ProfileSerializer, DeliveryAddressSerializer
from user_profile.permissions import IsOwnerOrAdmin


User = get_user_model()

# Create your views here.
class ProfileViewSet(mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrAdmin]


    def partial_update(self, request, *args, **kwargs):
        # partial = kwargs.pop('partial', False)
        # profile = self.get_object()
        
        # serializer = ProfileSerializer(
        #     profile,
        #     context={'request': request},
        #     data=request.data,
        #     partial=True
        # )

        
        # print("############################")
        # serializer.is_valid()
        # print(serializer.errors)
        # print("############################")
        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = ProfileSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid()

        print("#########################")
        print(serializer.errors)
        print("#########################")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class DeliveryAddressViewSet(mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer

    # def create(self, request, *args, **kwargs):
    #     print("##############################")
    #     print(request.data)
    #     serializer = DeliveryAddressSerializer(data=request.data, context={'request': request})
    #     print(serializer.is_valid())
    #     print("##################")
    #     print(serializer.errors)
    #     print("##############################")
    #     return super().create(request, *args, **kwargs)