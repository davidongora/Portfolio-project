from django.shortcuts import render
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.
class RegisterUserView(APIView):
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        gender = request.POST.get('gender', '')

        if not all([username, email, password]):
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username or email already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
            if cursor.fetchone()[0] > 0:
                return Response({"detail": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = make_password(password)
            cursor.execute('''INSERT INTO users (username, email, password, first_name, last_name, phone_number, gender) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           [username, email, hashed_password, first_name, last_name, phone_number, gender])
            return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)

    
    
from django.contrib.auth.hashers import check_password

class LoginUserView(APIView):
    def post(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')

        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username = %s", [username])
            result = cursor.fetchone()
            
            if result is None:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            stored_password = result[0]
            
            if not check_password(password, stored_password):
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)




@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recipient_email = data.get('recipient_email')
            subject = data.get('subject')
            message = data.get('message')
            
            if not recipient_email or not subject or not message:
                return JsonResponse({"error": "All fields are required."}, status=400)

            send_mail(
                subject,
                message,
                'your-email@example.com',  # From email address
                [recipient_email],
                fail_silently=False,
            )
            return JsonResponse({"success": "Email sent successfully!"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
