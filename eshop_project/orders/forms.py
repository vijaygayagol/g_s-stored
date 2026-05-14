# orders/forms.py

from django import forms
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress

        fields = [
            'full_name',
            'phone',
            'address',
            'city',
            'state',
            'pincode'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Complete Address'
            }),

            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),

            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State'
            }),

            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pincode'
            }),
        }