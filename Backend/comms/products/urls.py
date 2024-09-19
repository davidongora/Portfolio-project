from django.urls import path
from .views import ListProductsView, ProductDetailView, search_products, ShowTables

urlpatterns = [
    path('products/', ListProductsView.as_view(), name='list-products'),
    path('detail/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', search_products.as_view(), name='search-products'),
    path('tables/', ShowTables.as_view(), name='ShowTables'),


]
