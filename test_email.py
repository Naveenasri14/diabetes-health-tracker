# test_email.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diabetes_tracker.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("="*50)
print("🔍 TESTING EMAIL CONFIGURATION")
print("="*50)
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"Password length: {len(settings.EMAIL_HOST_PASSWORD)} characters")
print("="*50)

try:
    send_mail(
        subject='🔔 TEST FROM DIABETES TRACKER',
        message='If you see this, email is working!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['sobanarani0801@gmail.com'],
        fail_silently=False,
    )
    print("✅ Email sent successfully!")
    print("📧 Check your inbox in a few minutes")
except Exception as e:
    print(f"❌ Email failed: {e}")
    print(f"❌ Error type: {type(e).__name__}")
