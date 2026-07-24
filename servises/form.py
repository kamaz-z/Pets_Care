from django import forms
from .models import Order

class Order_Servises_form(forms.ModelForm):

    class Meta:
        model = Order

        fields = [
            'service',
            'employee',
            'order_date'
        ]

        widgets = {
            'service': forms.Select(
                attrs={'class': 'input-group'}
            ),

            'employee': forms.Select(
                attrs={'class': 'input-group'}
            ),

            'order_date': forms.DateTimeInput(
                attrs={
                    'class': 'input-group',
                    'type': 'datetime-local'
                }
            )
        }