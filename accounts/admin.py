"""
Admin configuration for accounts app.
v1.1 - Admin interface for OTP verification model
"""

from django.contrib import admin
from .models import OTPVerification


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    """Admin interface for OTP verification records"""
    list_display = ['user', 'created_at', 'is_used', 'is_expired']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['otp_hash', 'created_at']
    
    def is_expired(self, obj):
        """Display if OTP is expired"""
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'