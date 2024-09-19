from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class AddToCartView(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        # Validate required fields
        if not user_id:
            return Response({"detail": "Missing user_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not product_id:
            return Response({"detail": "Missing product_id"}, status=status.HTTP_400_BAD_REQUEST)
        if not quantity:
            return Response({"detail": "Missing quantity"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Check if user exists
                cursor.execute("SELECT id FROM users WHERE id = %s", [user_id])
                user_exists = cursor.fetchone()
                if not user_exists:
                    return Response({"detail": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Check if product exists (assuming a product check is also needed)
                cursor.execute("SELECT id FROM products WHERE id = %s", [product_id])
                product_exists = cursor.fetchone()
                if not product_exists:
                    return Response({"detail": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST)

                # Check if the product is already in the user's cart
                cursor.execute("SELECT id FROM shopping_cart WHERE user_id = %s AND product_id = %s", [user_id, product_id])
                result = cursor.fetchone()

                if result:
                    # Update the quantity if item already exists
                    cursor.execute("UPDATE shopping_cart SET quantity = quantity + %s WHERE id = %s", [quantity, result[0]])
                else:
                    # Add new item to the cart
                    cursor.execute("INSERT INTO shopping_cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                                   [user_id, product_id, quantity])

                return Response({"detail": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class UpdateCartView(APIView):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        quantity = request.POST.get('quantity')

        if not all([cart_id, quantity]):
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE shopping_cart SET quantity = %s WHERE id = %s", [quantity, cart_id])
                return Response({"detail": "Cart item updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartView(APIView):
    def post(self, request):
        cart_id = request.POST.get('cart_id')

        if not cart_id:
            return Response({"detail": "Cart ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM shopping_cart WHERE id = %s", [cart_id])
                return Response({"detail": "Item removed from cart successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ViewCartView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT sc.id, p.name, p.price, sc.quantity
                    FROM shopping_cart sc
                    JOIN products p ON sc.product_id = p.id
                    WHERE sc.user_id = %s
                ''', [user_id])
                
                cart_items = cursor.fetchall()
                cart_list = [
                    {
                        'id': item[0],
                        'name': item[1],
                        'price': item[2],
                        'quantity': item[3],
                    }
                    for item in cart_items
                ]
                
                return Response(cart_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
