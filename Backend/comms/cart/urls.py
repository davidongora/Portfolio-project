from django.urls import path
from .views import AddToCartView, UpdateCartView, RemoveFromCartView, ViewCartView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('update/', UpdateCartView.as_view(), name='update-cart'),
    path('remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('view/', ViewCartView.as_view(), name='view-cart'),
]
