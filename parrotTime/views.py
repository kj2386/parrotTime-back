from rest_framework import generics
from .serializers import ParrotSerializer
from .models import Parrot

class ParrotList(generics.ListCreateAPIView):
    queryset = Parrot.objects.all()
    serializer_class = ParrotSerializer
