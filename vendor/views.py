from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, permission_classes
from vendor.models import Vendor
from vendor.permissions import IsOwnerOrReadOnly
from vendor.serializers import VendorSerializer


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
    `create` - Only Authenticated users can create vendors (1 User : 1 Vendor)
    `list` - Any user can access vendor list
    `retrieve` - Any user can retrieve vendor detail
    `update` - Only vendor itself can update their detail
    `destroy` - Only vendor itself can destroy their record 
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
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]