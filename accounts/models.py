"""
Models for the accounts app.
v1.1 - OTP verification model for forgot password functionality
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import hashlib


class OTPVerification(models.Model):
    """
    Model to store OTP for password reset functionality.
    OTPs are valid for 5 minutes and are hashed for security.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_hash = models.CharField(max_length=64)  # SHA-256 hash of OTP
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def is_expired(self):
        """Check if OTP is expired (5 minutes validity)"""
        expiry_time = self.created_at + timedelta(minutes=5)
        return timezone.now() > expiry_time
    
    def verify_otp(self, otp):
        """Verify the provided OTP against stored hash"""
        otp_hash = hashlib.sha256(str(otp).encode()).hexdigest()
        return self.otp_hash == otp_hash and not self.is_expired() and not self.is_used
    
    @staticmethod
    def create_otp(user, otp):
        """Create a new OTP record with hashed OTP"""
        otp_hash = hashlib.sha256(str(otp).encode()).hexdigest()
        return OTPVerification.objects.create(user=user, otp_hash=otp_hash)
    
    def __str__(self):
        return f"OTP for {self.user.email} - Created: {self.created_at}"