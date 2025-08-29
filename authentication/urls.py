from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('verify/', views.verify_otp_view, name="verify_otp"),
    
    
        # urls.py
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-forgot-otp/', views.verify_forgot_otp_view, name='verify_forgot_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),



             ]