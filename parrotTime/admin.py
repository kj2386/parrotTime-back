from django.contrib import admin
from .models import Parrot, OrderItem, Order, Address, Payment


admin.site.register(Parrot)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Payment)
