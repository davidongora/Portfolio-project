from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ViewOrderItemsView(APIView):
    def get(self, request):
        order_id = request.GET.get('order_id')

        if not order_id:
            return Response({"detail": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Fetch order items details
                cursor.execute('''
                    SELECT oi.product_id, p.name, p.price, oi.quantity, oi.price_at_purchase
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                ''', [order_id])
                
                order_items = cursor.fetchall()
                
                items_list = [
                    {
                        "product_id": item[0],
                        "name": item[1],
                        "price": item[2],
                        "quantity": item[3],
                        "price_at_purchase": item[4],
                    }
                    for item in order_items
                ]
                
                return Response(items_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateOrderItemQuantityView(APIView):
    def post(self, request):
        order_id = request.POST.get('order_id')
        product_id = request.POST.get('product_id')
        new_quantity = request.POST.get('quantity')

        if not all([order_id, product_id, new_quantity]):
            return Response({"detail": "Order ID, Product ID, and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_quantity = int(new_quantity)
            if new_quantity <= 0:
                return Response({"detail": "Quantity must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
            
            with connection.cursor() as cursor:
                # Check if the order item exists
                cursor.execute("SELECT id FROM order_items WHERE order_id = %s AND product_id = %s", [order_id, product_id])
                if not cursor.fetchone():
                    return Response({"detail": "Order item not found"}, status=status.HTTP_404_NOT_FOUND)
                
                # Update the order item quantity
                cursor.execute("UPDATE order_items SET quantity = %s WHERE order_id = %s AND product_id = %s", [new_quantity, order_id, product_id])
                
                return Response({"detail": "Order item quantity updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteOrderItemView(APIView):
    def post(self, request):
        order_id = request.POST.get('order_id')
        product_id = request.POST.get('product_id')

        if not all([order_id, product_id]):
            return Response({"detail": "Order ID and Product ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Check if the order item exists
                cursor.execute("SELECT id FROM order_items WHERE order_id = %s AND product_id = %s", [order_id, product_id])
                if not cursor.fetchone():
                    return Response({"detail": "Order item not found"}, status=status.HTTP_404_NOT_FOUND)
                
                # Delete the order item
                cursor.execute("DELETE FROM order_items WHERE order_id = %s AND product_id = %s", [order_id, product_id])
                
                return Response({"detail": "Order item deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
