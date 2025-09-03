"""
URL configuration for accounts app.
v1.1 - Authentication related URLs
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('otp-verification/', views.OTPVerificationView.as_view(), name='otp_verification'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
]