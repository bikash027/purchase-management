from django import forms
from .models import PurchaseRequest

class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = [
            'purpose', 'specification', 'totalCost'
        ]