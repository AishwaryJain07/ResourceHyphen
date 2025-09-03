from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views import View
import random
import string

from .forms import (
    CustomUserCreationForm, LoginForm, ForgotPasswordForm,
    OTPVerificationForm, ResetPasswordForm
)
from .models import OTPVerification

@method_decorator([csrf_protect, never_cache], name='dispatch')
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self.redirect_authenticated_user(request.user)
        
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    return self.redirect_authenticated_user(user)
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
        
        return render(request, 'accounts/login.html', {'form': form})
    
    def redirect_authenticated_user(self, user):
        if user.is_staff:
            return redirect('dashboard:admin_dashboard')
        else:
            return redirect('dashboard:user_dashboard')

@method_decorator([csrf_protect, never_cache], name='dispatch')
class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
        
        return render(request, 'accounts/signup.html', {'form': form})

@method_decorator([csrf_protect, never_cache], name='dispatch')
class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        return render(request, 'accounts/forgot_password.html', {'form': form})
    
    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            otp = ''.join(random.choices(string.digits, k=6))
            OTPVerification.create_otp(user, otp)
            
            print(f"OTP for {email}: {otp}")  # For demo - remove in production
            
            request.session['reset_email'] = email
            messages.success(request, f'OTP sent to your email address. (Demo OTP: {otp})')
            return redirect('accounts:otp_verification')
        
        return render(request, 'accounts/forgot_password.html', {'form': form})

@method_decorator([csrf_protect, never_cache], name='dispatch')
class OTPVerificationView(View):
    def get(self, request):
        if 'reset_email' not in request.session:
            return redirect('accounts:forgot_password')
        
        form = OTPVerificationForm()
        return render(request, 'accounts/otp_verification.html', {'form': form})
    
    def post(self, request):
        if 'reset_email' not in request.session:
            return redirect('accounts:forgot_password')
        
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            email = request.session['reset_email']
            
            try:
                user = User.objects.get(email=email)
                otp_record = OTPVerification.objects.filter(
                    user=user, is_used=False
                ).first()
                
                if otp_record and otp_record.verify_otp(otp):
                    otp_record.is_used = True
                    otp_record.save()
                    
                    request.session['otp_verified'] = True
                    messages.success(request, 'OTP verified successfully.')
                    return redirect('accounts:reset_password')
                else:
                    messages.error(request, 'Invalid or expired OTP.')
                    
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        
        return render(request, 'accounts/otp_verification.html', {'form': form})

@method_decorator([csrf_protect, never_cache], name='dispatch')
class ResetPasswordView(View):
    def get(self, request):
        if not request.session.get('otp_verified') or 'reset_email' not in request.session:
            return redirect('accounts:forgot_password')
        
        form = ResetPasswordForm()
        return render(request, 'accounts/reset_password.html', {'form': form})
    
    def post(self, request):
        if not request.session.get('otp_verified') or 'reset_email' not in request.session:
            return redirect('accounts:forgot_password')
        
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = request.session['reset_email']
            password = form.cleaned_data['password1']
            
            try:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                
                del request.session['reset_email']
                del request.session['otp_verified']
                
                messages.success(request, 'Password reset successfully! Please log in.')
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        
        return render(request, 'accounts/reset_password.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')