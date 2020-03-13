from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('parrots', views.ParrotList.as_view(), name='parrot_list'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),
    path('order-summary/', views.OrderDetailView.as_view(), name='order-summary/'),
    path('checkout/', views.PaymentView.as_view(), name='checkout')

]
