from rest_framework import serializers
from orders.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Order
        fields = [
            'url',
            'id',
            'customer',
            'vendor',
            'product',
            'carrier',
            'price',
            'quantity',
            'discount',
            'total',
            'delivered',
            'cancelled',
            'paid',
            'delivery_address',
            'created_at',
            'updated_at',
            'delivered_at',
        ]
