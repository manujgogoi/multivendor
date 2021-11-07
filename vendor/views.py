from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from vendor import serializers
from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from vendor.permissions import IsOwnerOrReadOnly

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
class VendorViewSet(
                        mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet
                    
                    ):
    '''
    Vendor viewset provides `create`, `list`, `retrieve`, `update`,
    and `destroy` actions.
    Only Authenticated users can `create` vendors (1 User : 1 Vendor).
    Any user can access vendor `list`.
    Any user can `retrieve` vendor detail
    Only vendor itself can `update` their name
    Only vendor itself can `destroy` their record 
    '''
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        # Check user already has a vendor or not
        user = self.request.user
        vendor = user.vendor if hasattr(user, 'vendor') else None
        if vendor is not None:
            return Response({"error": [f"User {user.email} already has a vendor named {user.vendor}"]}, 
            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

        