from . import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('deposit/', views.deposit, name='deposit'),
    path('plans/', views.plans, name='plans'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('send-html-email/', views.send_html_email, name='send_html_email'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success_page'),

]
