from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Balance, Deposit, Withdrawal
from django.core.mail import send_mail
from django.conf import settings
from .forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from .forms import EmailMessageForm, WithdrawalForm
from .models import Withdrawal, Balance


@login_required
def dashboard(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    deposits = Deposit.objects.filter(user=request.user).order_by('-created_at')
    withdrawals = Withdrawal.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'balance': balance,
        'deposits': deposits,
        'withdrawals': withdrawals,
    }
    return render(request, 'dashboard.html', context)


@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.status = 'pending'
            deposit.save()
            # Email to admin
            send_mail(
                subject='New Deposit Submitted',
                message=f'User: {request.user.email}\nAmount: {deposit.amount}\nDescription: {deposit.description}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            return redirect('dashboard')
    else:
        form = DepositForm()
        
    wallet_addresses = {
        "BTC (Bitcoin)": "bc1qzm88yeqyh0y8k0ckrasr3u2fh3mkqc79fuw3hm",
        "ETH (Ethereum)": "0x54a7cdC51508Dd2335Db2Ad5ce4EE1CAb9Ac4F16",
        "USDT (Tether)": "0x54a7cdC51508Dd2335Db2Ad5ce4EE1CAb9Ac4F16",
        "TRX (Tron)": "TQQkwqsrUrbjiiToruqg4E3FoE6TYzg91G",
    }
    return render(request, 'deposit.html', {
        'form': form,
        'wallet_addresses': wallet_addresses,
    })


@login_required
def withdraw(request):
    user = request.user
    if request.method == 'POST':
        form = WithdrawalForm(request.POST, user=user)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = user
            withdrawal.status = 'pending'
            withdrawal.save()

            # Send to admin
            send_mail(
                subject='Withdrawal Request Submitted',
                message=(
                    f"User: {user.email}\n"
                    f"Email entered: {withdrawal.email}\n"
                    f"Amount: {withdrawal.amount}\n"
                    f"BTC Address: {withdrawal.bitcoin_address}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )

        

            return redirect('transaction_history')
    else:
        form = WithdrawalForm(user=user)

    return render(request, 'withdraw.html', {'form': form})



@login_required
def plans(request):
    return render(request, 'plans.html')


@login_required
def transaction_history(request):
    deposits = Deposit.objects.filter(user=request.user).order_by('-created_at')
    withdrawals = Withdrawal.objects.filter(user=request.user).order_by('-created_at')
    balance, created = Balance.objects.get_or_create(user=request.user)
    
    
    
    return render(request, 'transaction_history.html', {
        'deposits': deposits,
        'withdrawals': withdrawals,
        'balance': balance,
    })




@login_required
def send_html_email(request):
    if request.method == 'POST':
        form = EmailMessageForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['email']
            message_content = form.cleaned_data['message']

            subject = "Custom HTML Message"
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [recipient_email]

            # Plain text version (fallback)
            text_content = message_content

            # HTML version
            html_content = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; color: #333;">
                        <h2 style="color: #2c3e50;">Dear save before spending user,</h2>
                        <p>{message_content}</p>
                        <p style="margin-top: 20px; font-size: 12px; color: gray;">
                            This email was sent from {request.user.email}.
                        </p>
                    </body>
                </html>
            """

            msg = EmailMultiAlternatives(subject, text_content, from_email, to)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('success_page')  # Change to your success URL
    else:
        form = EmailMessageForm()

    return render(request, 'send_message.html', {'form': form})



def test_404(request):
    return render(request, "404.html", status=404)