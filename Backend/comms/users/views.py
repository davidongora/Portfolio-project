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
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegisterUserView(APIView):
    def post(self, request):
        
        username = first_name + last_name
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')

        if not all([username]):
            return Response({"detail": "Missing username required fields"}, status=status.HTTP_400_BAD_REQUEST)

        if not all([email]):
                    return Response({"detail": "Missing email required fields"}, status=status.HTTP_400_BAD_REQUEST)

        if not all([ password]):
                    return Response({"detail": "Missing  password required fields"}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", [username])
            if cursor.fetchone()[0] > 0:
                return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", [email])
            if cursor.fetchone()[0] > 0:
                return Response({"detail": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = make_password(password)
            cursor.execute('''INSERT INTO users (username, email, password, first_name, last_name, phone_number) 
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           [username, email, hashed_password, first_name, last_name, phone_number])
            subject = "Welcome to Our Platform"
            message = f"Hi {first_name},\n\nThank you for registering! Feel free to shop and explore our platform."
            send_mail(
                subject,
                message,
                'ongoradavid5@gmail.com', 
                [email],  
                fail_silently=False,
            )
            return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')

        if not username or not password:
            return Response({"detail": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Fetch user record by username
                cursor.execute("SELECT id, email, password FROM users WHERE username = %s", [username])
                result = cursor.fetchone()

                if result is None:
                    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

                # Unpack the result
                user_id, email, stored_password = result

                # Check if the provided password matches the stored password
                if not check_password(password, stored_password):
                    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

                # Clear any existing session before setting a new one
                request.session.flush()

                # Store user_id in session
                request.session['user_id'] = user_id  # This stores the user_id in the session
                return Response({"detail": "Login successful", "user_id": user_id, "email": email}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class SendEmail(APIView):
    def post(self, request):
        try:
            recipient_email = request.POST.get('recipient_email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Check if required fields are present
            if not recipient_email or not subject or not message:
                return JsonResponse({"error": "All fields are required."}, status=400)

            send_mail(
                subject,
                message,
                'ongoradavid5@gmail.com',  # Sender email address
                [recipient_email],
                fail_silently=False,
            )
            return JsonResponse({"success": "Email sent successfully!"}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)