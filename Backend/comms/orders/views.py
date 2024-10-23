import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection, transaction
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateOrderView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='Description of field1'),
                # 'field2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Description of field2'),
            },
            required=['user_id']
        ),
        responses={
            200: openapi.Response(
                description='Successful Response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'order_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the created object'),
                        # 'field1': openapi.Schema(type=openapi.TYPE_STRING, description='Description of field1'),
                        # 'field2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Description of field2'),
                    }
                )
            ),
            400: 'Bad Request'
        }
    )
    
    def post(self, request):
        # Get user_id from the session
        
        user_id = request.session.get('user_id')

        if not user_id:
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        cart_items_str = request.POST.get('cart_items', '[]')  # Expecting JSON string

        print(cart_items_str, 'your cart items')
        if not all([user_id, shipping_address, payment_method]):
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Parse cart_items from JSON string to list of dictionaries
            cart_items = json.loads(cart_items_str)

            if not isinstance(cart_items, list):
                return Response({"detail": "Invalid cart items format"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():  # Begin transaction
                # Calculate total price
                total_price = 0
                for item in cart_items:
                    if not isinstance(item, dict):
                        return Response({"detail": "Invalid item format in cart_items"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')

                    if not all([product_id, quantity]):
                        return Response({"detail": "Missing product_id or quantity in cart_items"}, status=status.HTTP_400_BAD_REQUEST)

                    with connection.cursor() as cursor:
                        cursor.execute("SELECT price FROM products WHERE id = %s", [product_id])
                        product_price = cursor.fetchone()

                        if product_price is None:
                            return Response({"detail": f"Product with id {product_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

                        product_price = product_price[0]
                        total_price += product_price * quantity

                # Create the order
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO orders (user_id, total_price, status, created_at) VALUES (%s, %s, 'Pending', NOW())",
                        [user_id, total_price]
                    )
                    order_id = cursor.lastrowid

                    # Fetch user's email
                    cursor.execute("SELECT email FROM users WHERE id = %s", [user_id])
                    email_result = cursor.fetchone()

                    if email_result is None:
                        return Response({"detail": "Email not found for user"}, status=status.HTTP_400_BAD_REQUEST)

                    email = email_result[0]  # Get the email from the result tuple

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

                # Send confirmation email to the user (you can add cart items in this email as well)
                subject = "Your Order Confirmation"
                message = f"Hi, your order with ID {order_id} with {cart_items} has been  placed successfully. Thank you for shopping!"
                send_mail(
                    subject,
                    message,
                    'ongoradavid5@gmail.com',  # Sender email address
                    [email],  # Recipient's email address
                    fail_silently=False,
                )

                # Return success response
                return Response({"detail": "Order created successfully", "order_id": order_id}, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return Response({"detail": "Invalid JSON format for cart_items"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ViewOrderDetailsView(APIView):
    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'field1': openapi.Schema(type=openapi.TYPE_STRING, description='Description of field1'),
    #             'field2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Description of field2'),
    #         },
    #         required=['field1', 'field2']
    #     ),
    #     responses={
    #         200: openapi.Response(
    #             description='Successful Response',
    #             schema=openapi.Schema(
    #                 type=openapi.TYPE_OBJECT,
    #                 properties={
    #                     'order_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID of the created object'),
    #                     # 'field1': openapi.Schema(type=openapi.TYPE_STRING, description='Description of field1'),
    #                     # 'field2': openapi.Schema(type=openapi.TYPE_INTEGER, description='Description of field2'),
    #                 }
    #             )
    #         ),
    #         400: 'Bad Request'
    #     }
    # )
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
