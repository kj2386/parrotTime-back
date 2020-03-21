from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('user-id/', views.UserIdView.as_view(), name='user-id'),
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('addresses/create/', views.AddressCreateView.as_view(),
         name='address_create'),
    path('parrots', views.ParrotList.as_view(), name='parrot_list'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),
    path('order-summary/', views.OrderDetailView.as_view(), name='order-summary/'),
    path('checkout/', views.PaymentView.as_view(), name='checkout'),


]
