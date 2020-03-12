from rest_framework import serializers
from .models import Parrot

class ParrotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parrot
        fields = ('id', 'name', 'slug', 'price', 'gif_url')