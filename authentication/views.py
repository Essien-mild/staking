from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from . utils import * 
from django.utils import timezone
from .utils import send_otp_email
from django.views.decorators.cache import never_cache


User = get_user_model()
from django.core.mail import send_mail



@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_email_verified:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Please verify your email before logging in.", extra_tags='login')
                return redirect('login')

        messages.error(request, "Invalid login credentials", extra_tags='login')
        return redirect('login')

    return render(request, 'login.html')


@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')

        if not username or not email or not password or not password_confirm:
            messages.error(request, "Please fill in all fields.", extra_tags='register')
            return redirect('register')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.", extra_tags='register')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters", extra_tags='register')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.", extra_tags='register')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.", extra_tags='register')
            return redirect('register')
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        send_otp_email(user)

        request.session['user_email'] = email

        messages.success(request, "Account created. Check your email for the OTP.",)
        return redirect('verify_otp')

    return render(request, 'register.html')





def logout_view(request):
    logout(request)
    return redirect('login')


def verify_otp_view(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        email = request.session.get("user_email")

        try:
            user = get_user_model().objects.get(email=email)

            # Validate OTP
            if user.otp_code == otp_input and timezone.now() < user.otp_expiry:
                user.is_email_verified = True
                user.otp_code = ''
                user.save()

                # Auto-login
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                #messages.success(request, "Email verified and logged in successfully.")
                return redirect('dashboard')  
            else:
                messages.error(request, "Invalid or expired OTP.")
                return redirect('verify_otp')

        except get_user_model().DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('register')

    return render(request, 'verify_otp.html')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            send_otp_email(user)
            request.session['reset_email'] = email
            messages.success(request, "OTP sent to your email.")
            return redirect('verify_forgot_otp')
        except User.DoesNotExist:
            messages.error(request, "No user with this email.")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def verify_forgot_otp_view(request):
    if request.method == 'POST':
        otp_input = request.POST.get("otp")
        email = request.session.get("reset_email")
        try:
            user = User.objects.get(email=email)

            if user.otp_code == otp_input and timezone.now() < user.otp_expiry:
                user.otp_code = ''
                user.save()
                request.session['reset_otp_verified'] = True
                messages.success(request, "OTP verified. Please reset your password.")
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid or expired OTP.")
                return redirect('verify_forgot_otp')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')

    return render(request, 'verify_forgot_otp.html')


def reset_password_view(request):
    if not request.session.get('reset_otp_verified'):
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')
        if len(password1) < 6:
            messages.error(request, "Password too short.")
            return redirect('reset_password')

        email = request.session.get('reset_email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()

            # Clear session
            request.session.pop('reset_email')
            request.session.pop('reset_otp_verified')

            # Auto-login
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            messages.success(request, "Password reset successful. You are now logged in.")
            return redirect('dashboard')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')

    return render(request, 'reset_password.html')
