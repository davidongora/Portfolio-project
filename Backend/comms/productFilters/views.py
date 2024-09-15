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
            try:
                cursor.execute(
                    """INSERT INTO product_filters (product_id, filter_type, filter_value) VALUES (%s, %s, %s)""",
                    [product_id, filter_type, filter_value]
                )
                connection.commit()  
                return Response('record inserted', status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

class getFilters(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            try:
                cursor.execute('''SELECT * FROM product_filters''')
                filters_list = cursor.fetchall()
                return Response(filters_list, status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)