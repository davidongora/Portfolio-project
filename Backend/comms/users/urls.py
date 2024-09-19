from django.urls import path

from .views import RegisterUserView, LoginUserView, SendEmail

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('send-email/', SendEmail.as_view(), name='send-email'),

]
