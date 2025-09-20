from django.conf import settings
from django.core.mail import send_mail
import random
import string
from django.contrib.auth import get_user_model
User = get_user_model() 

def send_otp_email (email,otp):
    subject="رمز التحقق لحسابك"
    message=f"مرحبا رمز التحقق الخاص بك هو:{otp}"
    from_email=settings.DEFAULT_FROM_EMAIL
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list)

def generate_unique_username(length=8):
        while True:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            if not User.objects.filter(username=username).exists():
                return username
