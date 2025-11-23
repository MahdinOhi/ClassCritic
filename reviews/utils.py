import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def generate_otp():
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(student_email, otp):
    """Send OTP to student email"""
    subject = 'ClassCritic - Your OTP for Verification'
    message = f"""
    Hello,
    
    Your OTP for ClassCritic verification is: {otp}
    
    This OTP will expire in 5 minutes.
    
    If you didn't request this OTP, please ignore this email.
    
    Best regards,
    ClassCritic Team
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [student_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def word_count(text):
    """Count words in text"""
    return len(text.split())


def is_otp_valid(otp_created_at):
    """Check if OTP is still valid (within 5 minutes)"""
    if not otp_created_at:
        return False
    expiry_time = otp_created_at + timedelta(minutes=5)
    return timezone.now() < expiry_time
