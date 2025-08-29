import threading
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def authenticate(email, password):
    from .models import User
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
        return None
    except User.DoesNotExist:
        return None


def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP



def send_otp_email(user):
    otp = generate_otp()
    user.otp_code = otp
    user.otp_expiry = timezone.now() + timedelta(minutes=10)
    user.save()

    subject = "Verify your email with OTP"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    context = {'username': user.username, 'otp': otp}
    html_content = render_to_string('otp_email.html', context)
    text_content = f"Your verification code is: {otp}"

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    
def async_send_otp_email(user):
    threading.Thread(target=send_otp_email, args=(user,)).start()

