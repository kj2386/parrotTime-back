from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('user-id/', views.UserIdView.as_view(), name='user-id'),
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('addresses/create/', views.AddressCreateView.as_view(),
         name='address_create'),
    path('addresses/<pk>/update/', views.AddressUpdateView.as_view(),
         name='address_update'),
    path('addresses/<pk>/delete/', views.AddressDeleteView.as_view(),
         name='address_delete'),
    path('parrots', views.ParrotList.as_view(), name='parrot_list'),
    path('add-to-cart/', views.AddToCart.as_view(), name='add-to-cart'),
    path('order-summary/', views.OrderDetailView.as_view(), name='order-summary/'),
    path('checkout/', views.PaymentView.as_view(), name='checkout'),
    path('order-items/<pk>/delete/',
         views.OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('order-item/update-quantity/',
         views.OrderQuantityUpdateView.as_view(), name='order-item-update-quantity'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),

]
