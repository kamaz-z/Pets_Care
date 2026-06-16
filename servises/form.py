from django import forms
from .models import Order, Servises

class Order_Servises_form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service', 'customer_phone', 'order_date']
        widgets = {
            # Ось наш "гамбургер" (випадаючий список послуг)
            'service': forms.Select(attrs={'class': 'input-group'}),
            # Поле для телефону
            'customer_phone': forms.TextInput(attrs={
                'class': 'input-group', 
                'placeholder': '+380XXXXXXXXX'
            }),
            # Календар для вибору дати
            'order_date': forms.DateTimeInput(attrs={
                'class': 'input-group', 
                'type': 'date',
                'type_2':'time'
            }),
        }