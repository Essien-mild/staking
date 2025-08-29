from django import forms
from .models import Deposit
from .models import Withdrawal
from authentication.utils  import authenticate


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['amount', 'proof_image', 'description']



class WithdrawalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Withdrawal
        fields = ['email', 'amount', 'bitcoin_address', 'password']  # Added email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 2000:
            raise forms.ValidationError("Minimum withdrawal is $2,000.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        amount = cleaned_data.get("amount")

        if self.user:
            # Check password
            if not self.user.check_password(password):
                raise forms.ValidationError("Incorrect password.")

            # Check withdrawable balance
            if amount and self.user.balance.withdrawable < amount:
                raise forms.ValidationError(
                    f"Insufficient balance. Your balance is ${self.user.balance.withdrawable}."
                )



class EmailMessageForm(forms.Form):
    email = forms.EmailField(label="Recipient Email")
    message = forms.CharField(widget=forms.Textarea, label="Message")
