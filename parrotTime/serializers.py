from rest_framework import serializers
from .models import Parrot, OrderItem, Order


class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ParrotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parrot
        fields = ('id', 'name', 'slug', 'price', 'gif_url',)


class OrderItemSerializer(serializers.ModelSerializer):
    parrot = StringSerializer()
    parrot_obj = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'parrot', 'quantity', 'parrot_obj', )

    def get_parrot_obj(self, obj):
        return ParrotSerializer(obj.parrot).data


class OrderSerializer(serializers.ModelSerializer):
    order_parrots = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'order_parrots', 'total', )

    def get_order_parrots(self, obj):
        return OrderItemSerializer(obj.parrots.all(), many=True).data

    def get_total(self, obj):
        return obj.get_total()
