from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import ParrotSerializer, OrderSerializer
from .models import Parrot, OrderItem, Order


class ParrotList(generics.ListAPIView):
    queryset = Parrot.objects.all()
    serializer_class = ParrotSerializer


class AddToCart(APIView):
    def post(self, request, *args, **kwards):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response({'message': 'Ivalid request'}, status=HTTP_400_BAD_REQUEST)
        parrot = get_object_or_404(Parrot, slug=slug)
        order_parrot, created = OrderItem.objects.get_or_create(
            parrot=parrot,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.parrots.filter(parrot__slug=parrot.slug).exists():
                order_parrot.quantity += 1
                order_parrot.save()
                return Response(status=HTTP_200_OK)
            else:
                order.parrots.add(order_parrot)
                return Response(status=HTTP_200_OK)
        else:
            order = Order.objects.create(
                user=request.user
            )
            order.parrots.add(order_parrot)
            return Response(status=HTTP_200_OK)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return order
        except ObjectDoesNotExist:
            return Response({'message': 'You do not have an active order.'}, status=HTTP_400_BAD_REQUEST)
