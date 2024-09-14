from django.urls import path

from .views import CreateOrderView, ViewOrderDetailsView, ListOrdersView

urlpatterns = [
    path('order/create/', CreateOrderView.as_view(), name='create-order'),
    path('order/details/', ViewOrderDetailsView.as_view(), name='view-order-details'),
    path('orders/list/', ListOrdersView.as_view(), name='list-orders'),
]