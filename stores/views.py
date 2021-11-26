from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from stores.models import Category, Image, Product, Specification
from stores.serializers import CategorySerializer, ImageSerializer, ProductSerializer, SpecificationSerializer
from stores.permissions import ImagePermission, IsAdminOrReadOnly, SpecificationPermission

User = get_user_model()

# Create your views here.
class CategoryViewSet(mixins.CreateModelMixin, 
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    '''
    This viewset provides `list`, `create`, `update`, `retrieve`, 
    and `destroy` actions for Category
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    
    '''
    This viewset provides `list`, `create`, `update`, `retrieve`, 
    and `destroy` actions for Products
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.filter(is_active=True, vendor__is_active=True)
        serializer = ProductSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


    def update(self, request, *args, **kwargs):

        queryset = Product.objects.all()
        partial = kwargs.pop('partial', False)
        product = self.get_object()
        user = request.user
        user_vendor = user.vendor if hasattr(user, 'vendor') else None

        if user_vendor is not None:
            if user_vendor == product.vendor:     
                serializer = ProductSerializer(
                                                product, 
                                                context={'request': request}, 
                                                data=request.data,
                                                partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'This is not your product'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'You are not a vendor'}, status=status.HTTP_403_FORBIDDEN)


    def perform_create(self, serializer):
        vendor = self.request.user.vendor
        serializer.save(vendor=vendor)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user_vendor = user.vendor if hasattr(user, 'vendor') else None

        if user_vendor is not None:
            product = self.get_object()
            if user_vendor == product.vendor:      
                self.perform_destroy(product)
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({'error': 'You are not allowed'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'You are not a vendor'}, status=status.HTTP_403_FORBIDDEN)

    

class ImageViewSet(
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [ImagePermission]

class SpecificationViewSet(
                            mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [SpecificationPermission]