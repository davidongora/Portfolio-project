from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class AddFilters(APIView):
    
    def post(self, request):
        product_id = request.POST.get('product_id')
        filter_type = request.POST.get('filter_type')
        filter_value = request.POST.get('filter_value')
        
        with connection.cursor() as cursor:
            cursor.execute(
            '''INSERT INTO product_filters ('product_id,'
'filter_type', 'filter_value') VALUES (%s,%s,%s,) '''),
            [product_id,filter_type,filter_value]
            
            
            return Response('record inserted', status.HTTP_200_OK)
            
class getFilters(APIView):
    def get(self, request):
        
        with connection.cursor() as cursor:
            filters = cursor.execute('''SELECT * FROM users''') 
            
            return Response(filters, status.HTTP_200_OK)