from rest_framework import serializers, viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django.contrib.auth import get_user_model
from stores.models import Category
from stores.serializers import CategorySerializer
from stores.permissions import IsAdminOrReadOnly

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
    pass