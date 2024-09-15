from django.urls import path
from .views import ViewOrderItemsView, UpdateOrderItemQuantityView, DeleteOrderItemView

urlpatterns = [
    path('view/', ViewOrderItemsView.as_view(), name='view-order-items'),
    path('update-quantity/', UpdateOrderItemQuantityView.as_view(), name='update-order-item-quantity'),
    path('delete/', DeleteOrderItemView.as_view(), name='delete-order-item'),
]
