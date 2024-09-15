from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


class ListProductsView(APIView):
    def get(self, request):
        category = request.GET.get('category', None)
        gender = request.GET.get('gender', None)
        size = request.GET.get('size', None)
        search_query = request.GET.get('search', '')

        try:
            with connection.cursor() as cursor:
                query = 'SELECT * FROM products WHERE name LIKE %s'
                params = ['%' + search_query + '%']

                if category:
                    query += ' AND category = %s'
                    params.append(category)

                if gender:
                    query += ' AND gender = %s'
                    params.append(gender)

                if size:
                    query += ' AND size = %s'
                    params.append(size)

                cursor.execute(query, params)
                products = cursor.fetchall()

                product_list = [
                    {
                        "id": product[0],
                        "name": product[1],
                        "description": product[2],
                        "price": product[3],
                        "category": product[4],
                        "gender": product[5],
                        "size": product[6],
                        "image_url": product[7],
                        "created_at": product[8]
                    }
                    for product in products
                ]

                return Response(product_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')

        if not product_id:
            return Response({"detail": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT * FROM products WHERE id = %s
                ''', [product_id])
                
                product = cursor.fetchone()
                
                if not product:
                    return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

                product_detail = {
                    "id": product[0],
                    "name": product[1],
                    "description": product[2],
                    "price": product[3],
                    "category": product[4],
                    "gender": product[5],
                    "size": product[6],
                    "image_url": product[7],
                    "created_at": product[8]
                }
                
                return Response(product_detail, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
class search_products(APIView):
    def get(request):
        search_query = request.GET.get('search', '')
        category = request.GET.get('category', '')
        gender = request.GET.get('gender', '')
        size = request.GET.get('size', '')

        try:
            with connection.cursor() as cursor:
                query = 'SELECT * FROM products WHERE name LIKE %s'
                params = ['%' + search_query + '%']

                if category:
                    query += ' AND category = %s'
                    params.append(category)

                if gender:
                    query += ' AND gender = %s'
                    params.append(gender)

                if size:
                    query += ' AND size = %s'
                    params.append(size)

                cursor.execute(query, params)
                rows = cursor.fetchall()

                products = [
                    {
                        "id": row[0],
                        "name": row[1],
                        "description": row[2],
                        "price": row[3],
                        "category": row[4],
                        "gender": row[5],
                        "size": row[6],
                        "image_url": row[7],
                        "created_at": row[8]
                    }
                    for row in rows
                ]

                return JsonResponse(products, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
