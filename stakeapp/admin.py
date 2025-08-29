from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Balance, Deposit, Withdrawal
from django.utils.html import format_html


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'withdrawable', 'staking', 'saving')
    search_fields = ('user__email',)
    list_editable = ('withdrawable', 'staking', 'saving')
    ordering = ('user__email',)


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at', 'view_proof')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'description')
    ordering = ('-created_at',)
    list_editable = ('status',)

    def view_proof(self, obj):
        if obj.proof_image:
            return format_html("<a href='{}' target='_blank'>View</a>", obj.proof_image.url)
        return "No Image"
    view_proof.short_description = "Proof"


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'bitcoin_address', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'bitcoin_address')
    ordering = ('-created_at',)
    list_editable = ('status',)
