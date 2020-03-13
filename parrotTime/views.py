from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import ParrotSerializer, OrderSerializer
from .models import Parrot, OrderItem, Order
import stripe

stripe.api_key = 


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


class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = request.data.get('stripeToken')
        save = False
        use_default = False

        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token
            )

            order_parrots = order.parrots.all()
            order_parrots.update(ordered=True)
            for parrot in order_parrots:
                parrot.save()

            order.ordered = True
           
            order.save()

            return Response(status=HTTP_200_OK)

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            return Response({"message": f"{err.get('message')}"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return Response({"message": "Rate limit error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.InvalidRequestError as e:
            print(e)
            # Invalid parameters were supplied to Stripe's API
            return Response({"message": "Invalid parameters"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return Response({"message": "Not authenticated"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return Response({"message": "Network error"}, status=HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return Response({"message": "Something went wrong. You were not charged. Please try again."}, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            # send an email to ourselves
            print(e)
            return Response({"message": "A serious error occurred. We have been notifed."}, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "Invalid data received"}, status=HTTP_400_BAD_REQUEST)
