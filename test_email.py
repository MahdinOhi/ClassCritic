# SMTP Email Troubleshooting & Testing Script
# Run this to test your email configuration

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classcritic.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("ClassCritic Email Configuration Test")
print("=" * 60)

# Display current configuration
print("\nCurrent Email Settings:")
print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")

if 'smtp' in settings.EMAIL_BACKEND.lower():
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"   EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else '(NOT SET)'}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check for common issues
    print("\nConfiguration Check:")
    issues = []
    
    if not settings.EMAIL_HOST_USER:
        issues.append("ERROR: EMAIL_HOST_USER is not set in .env file")
    else:
        print(f"   OK: EMAIL_HOST_USER is set")
    
    if not settings.EMAIL_HOST_PASSWORD:
        issues.append("ERROR: EMAIL_HOST_PASSWORD is not set in .env file")
    else:
        print(f"   OK: EMAIL_HOST_PASSWORD is set")
    
    if settings.EMAIL_PORT != 587:
        issues.append(f"WARNING: EMAIL_PORT is {settings.EMAIL_PORT}, should be 587 for TLS")
    else:
        print(f"   OK: EMAIL_PORT is correct (587)")
    
    if not settings.EMAIL_USE_TLS:
        issues.append("WARNING: EMAIL_USE_TLS is False, should be True for Gmail")
    else:
        print(f"   OK: EMAIL_USE_TLS is enabled")
    
    if issues:
        print("\nIssues Found:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\nAll settings look good!")
    
    # Test email sending
    print("\nTesting Email Send...")
    print("   Enter a test email address (or press Enter to skip):")
    test_email = input("   > ").strip()
    
    if test_email:
        try:
            send_mail(
                subject='ClassCritic - Test Email',
                message='This is a test email from ClassCritic. If you receive this, your SMTP configuration is working correctly!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            print(f"\n   SUCCESS: Email sent successfully to {test_email}!")
            print("   Check your inbox (and spam folder)")
        except Exception as e:
            print(f"\n   ERROR sending email:")
            print(f"   {type(e).__name__}: {str(e)}")
            print("\n   Common Solutions:")
            print("   1. Make sure you're using an App Password, not your regular Gmail password")
            print("   2. Enable 2-Factor Authentication on your Gmail account")
            print("   3. Generate App Password at: https://myaccount.google.com/apppasswords")
            print("   4. Check that EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are correct in .env")
            print("   5. Make sure .env has EMAIL_BACKEND=smtp (not console)")
    else:
        print("   Skipped email test")
else:
    print("\nWARNING: Console backend is active - emails will print to console, not send via SMTP")
    print("   To enable SMTP, set EMAIL_BACKEND=smtp in your .env file")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
