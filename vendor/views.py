from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny, IsAuthenticated
from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from vendor.permissions import IsOwnerOrReadOnly

from django.contrib.auth import get_user_model

from stores.models import Product
from stores.serializers import ProductSerializer

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
    Any user can access active vendor `list`.
    Any user can `retrieve` active vendor detail
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

    # def get_queryset(self):
    #     if self.action == 'list':
    #         return Vendor.objects.filter(is_active=True)

    #     if self.action == 'retrieve':
    #         return Vendor.objects.filter(owner__id=User.id)

    #     return Vendor.objects.all()


    # Customize list view to list only active vendors
    def list(self, request, *args, **kwargs):
        queryset = Vendor.objects.filter(is_active=True)
        # context={'request':request} is required by Serializer with HyperlinkedRelatedField
        serializer = VendorSerializer(queryset, context={'request':request}, many=True)
        return Response(serializer.data)

    # viewset custom action to get vendor products
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        queryset = Vendor.objects.all()
        # vendor = get_object_or_404(queryset, pk=pk)
        # vendor_products = Product.objects.filter(vendor=vendor)
        vendor_products = Product.objects.all()
        serializer = ProductSerializer(vendor_products, context={'request':request}, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = Vendor.objects.all()
        vendor = get_object_or_404(queryset, pk=pk)
        if vendor.owner == request.user or vendor.is_active:
            serializer = VendorSerializer(vendor, context={'request':request})
            return Response(serializer.data)
        return Response({'detail':'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        '''
        Override create method of `CreateModelMixinClass`.
        If the authenticated user already has a vendor then it cannot
        create another vendor (Duplicate entry handling of OneToOneRelationship). 
        '''
        user = self.request.user
        vendor = user.vendor if hasattr(user, 'vendor') else None
        if vendor is not None:
            return Response({"detail": ["The User already has a vendor"]}, 
            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED) # , headers=headers

    def perform_create(self, serializer):
        '''
        Override this method to associate vendor with
        the Authenticated user
        '''
        serializer.save(owner=self.request.user)
