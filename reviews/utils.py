import random
import string
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


def generate_otp():
    """Generate a random 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(student_email, otp):
    """Send OTP to student email"""
    # Check if email backend is configured properly
    email_backend = getattr(settings, 'EMAIL_BACKEND', '')
    
    # Warn if using console backend (emails won't actually be sent)
    if 'console' in email_backend.lower():
        logger.warning(
            f"Email backend is set to console. OTP email for {student_email} "
            f"will be printed to console instead of being sent. "
            f"Set EMAIL_BACKEND=smtp in .env file to enable real email sending."
        )
    
    # Check if SMTP is configured but credentials are missing
    if 'smtp' in email_backend.lower():
        email_host_user = getattr(settings, 'EMAIL_HOST_USER', '')
        email_host_password = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
        
        if not email_host_user or not email_host_password:
            error_msg = (
                f"SMTP email backend is configured but EMAIL_HOST_USER or "
                f"EMAIL_HOST_PASSWORD is missing. Please check your .env file."
            )
            logger.error(error_msg)
            return False
    
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
        logger.info(f"OTP email sent successfully to {student_email}")
        return True
    except Exception as e:
        error_msg = f"Failed to send OTP email to {student_email}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        # Log helpful troubleshooting information
        if 'smtp' in email_backend.lower():
            logger.error(
                "SMTP Configuration Check:\n"
                f"  EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'NOT SET')}\n"
                f"  EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'NOT SET')}\n"
                f"  EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'NOT SET')}\n"
                f"  EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'NOT SET')}\n"
                f"  EMAIL_HOST_PASSWORD: {'SET' if getattr(settings, 'EMAIL_HOST_PASSWORD', '') else 'NOT SET'}\n"
                f"  DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'NOT SET')}"
            )
        
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
