from django.urls import path

from .views import RegisterUserView, LoginUserView, send_email

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('send-email/', send_email, name='send-email'),

]
