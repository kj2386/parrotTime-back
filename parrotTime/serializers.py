from rest_framework import serializers
from .models import Parrot, OrderItem, Order


class ParrotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parrot
        fields = ('name', 'slug', 'price', 'gif_url',)


