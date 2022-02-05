from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.models import Order
from orders.serializers import OrderSerializer
# Create your views here.


class OrderViewSet(mixins.CreateModelMixin, 
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['vendor', 'customer','cancelled','delivered', 'paid', 'created_at']
