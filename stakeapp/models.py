from django.db import models
from django.conf import settings
from django.utils import timezone

class Balance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    withdrawable = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    staking = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saving = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.email} - Balance"


class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('declined', 'Declined'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    proof_image = models.ImageField(upload_to='deposit_proofs/')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Deposit by {self.user.email} - {self.amount} ({self.status})"


class Withdrawal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('declined', 'Declined'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()  # NEW field for withdrawal email
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bitcoin_address = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Withdrawal by {self.user.email} - {self.amount} ({self.status})"
