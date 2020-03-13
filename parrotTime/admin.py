from django.contrib import admin
from .models import Parrot, OrderItem, Order


admin.site.register(Parrot)
admin.site.register(OrderItem)
admin.site.register(Order)
