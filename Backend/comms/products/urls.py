from django.urls import path
from .views import ListProductsView, ProductDetailView

urlpatterns = [
    path('products/', ListProductsView.as_view(), name='list-products'),
    path('detail/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', search_products, name='search-products'),

]
