from django import forms
from .models import Customer, ShippingAddress


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'name']


class ShippingAddressForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))

    class Meta:
        model = ShippingAddress
        fields = '__all__'
