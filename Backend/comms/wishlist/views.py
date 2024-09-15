from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class AddToWishlistView(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')

        if not all([user_id, product_id]):
            return Response({"detail": "User ID and Product ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Check if the product is already in the user's wishlist
                cursor.execute("SELECT id FROM wishlist WHERE user_id = %s AND product_id = %s", [user_id, product_id])
                result = cursor.fetchone()
                
                if result:
                    return Response({"detail": "Item already in wishlist"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Add new item to the wishlist
                cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (%s, %s)",
                               [user_id, product_id])
                
                return Response({"detail": "Item added to wishlist successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class RemoveFromWishlistView(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')

        if not all([user_id, product_id]):
            return Response({"detail": "User ID and Product ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM wishlist WHERE user_id = %s AND product_id = %s", [user_id, product_id])
                return Response({"detail": "Item removed from wishlist successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewWishlistView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')

        if not user_id:
            return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT p.id, p.name, p.price, p.description, p.image_url
                    FROM wishlist w
                    JOIN products p ON w.product_id = p.id
                    WHERE w.user_id = %s
                ''', [user_id])
                
                wishlist_items = cursor.fetchall()
                wishlist_list = [
                    {
                        'id': item[0],
                        'name': item[1],
                        'price': item[2],
                        'description': item[3],
                        'image_url': item[4],
                    }
                    for item in wishlist_items
                ]
                
                return Response(wishlist_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
