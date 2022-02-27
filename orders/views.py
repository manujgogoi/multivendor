from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.models import Order
from orders.serializers import OrderSerializer
from django.utils.timezone import now
# Create your views here.


class OrderViewSet(mixins.CreateModelMixin, 
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin, 
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['vendor', 'customer', 'carrier', 'cancelled','delivered', 'paid', 'created_at']

    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()


        """
        is delivered is True then add current datetime to delivered_at
        """
        if 'delivered' in request.data.keys():
            if request.data['delivered']:
                if request.data['delivered'] == True:
                    request.data['delivered_at'] = now()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



