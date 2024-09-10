from django.urls import path

from .views import getFilters

urlpatterns = [
    path('list_of_filters/', getFilters.as_view(), name='list_of_filters')
]
