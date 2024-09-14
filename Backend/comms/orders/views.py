from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class CreateOrderView(APIView):
    def post(self, request):
        user_id = request.POST.get('user_id')
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        cart_items = request.POST.get('cart_items')  # Expecting JSON list of {product_id, quantity}

        if not all([user_id, shipping_address, payment_method, cart_items]):
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Begin transaction
                connection.transaction.on_commit(lambda: None)

                # Calculate total price
                total_price = 0
                for item in cart_items:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')

                    cursor.execute("SELECT price FROM products WHERE id = %s", [product_id])
                    product_price = cursor.fetchone()[0]
                    total_price += product_price * quantity

                # Create the order
                cursor.execute(
                    "INSERT INTO orders (user_id, total_price, status, created_at) VALUES (%s, %s, 'Pending', NOW())",
                    [user_id, total_price]
                )
                order_id = cursor.lastrowid

                # Create order items
                for item in cart_items:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')

                    cursor.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
                        [order_id, product_id, quantity, product_price]
                    )

                # Clear the cart
                cursor.execute("DELETE FROM shopping_cart WHERE user_id = %s", [user_id])

                return Response({"detail": "Order created successfully", "order_id": order_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewOrderDetailsView(APIView):
    def get(self, request):
        order_id = request.GET.get('order_id')

        if not order_id:
            return Response({"detail": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Fetch order details
                cursor.execute('''
                    SELECT o.id, o.user_id, o.total_price, o.status, o.created_at
                    FROM orders o
                    WHERE o.id = %s
                ''', [order_id])
                
                order = cursor.fetchone()
                
                if not order:
                    return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

                # Fetch order items
                cursor.execute('''
                    SELECT oi.product_id, p.name, p.price, oi.quantity
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                ''', [order_id])
                
                order_items = cursor.fetchall()
                
                order_details = {
                    "order_id": order[0],
                    "user_id": order[1],
                    "total_price": order[2],
                    "status": order[3],
                    "created_at": order[4],
                    "items": [
                        {
                            "product_id": item[0],
                            "name": item[1],
                            "price": item[2],
                            "quantity": item[3],
                        }
                        for item in order_items
                    ]
                }
                
                return Response(order_details, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListOrdersView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id')
        is_admin = request.GET.get('is_admin', 'false').lower() == 'true'

        try:
            with connection.cursor() as cursor:
                if is_admin:
                    # List all orders for admin
                    cursor.execute('''
                        SELECT o.id, o.user_id, o.total_price, o.status, o.created_at
                        FROM orders o
                    ''')
                else:
                    # List orders for a specific user
                    if not user_id:
                        return Response({"detail": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

                    cursor.execute('''
                        SELECT o.id, o.user_id, o.total_price, o.status, o.created_at
                        FROM orders o
                        WHERE o.user_id = %s
                    ''', [user_id])

                orders = cursor.fetchall()
                orders_list = [
                    {
                        "order_id": order[0],
                        "user_id": order[1],
                        "total_price": order[2],
                        "status": order[3],
                        "created_at": order[4]
                    }
                    for order in orders
                ]
                
                return Response(orders_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
