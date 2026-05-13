from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Pets,Type_OF_PETS


class Register_Form(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'username': 'Ваш унікальний логін',
            'email': 'example@email.com',
            'password1': 'Придумайте пароль',
            'password2': 'Повторіть пароль'
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input-field',
                'placeholder': placeholders.get(field_name, '')
            })
class Pets_Register_Form(ModelForm):
    class Meta:
        model = Pets
        fields = ['type_pets', 'name', 'age', 'weight', 'passport_number']
        widgets = {
            'type_pets': forms.Select(attrs={'class': 'input-field'}),
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': "Ім'я улюбленця"}),
            'age': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Вік'}),
            'weight': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Вага (кг)'}),
            'passport_number': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Номер паспорта'}),
        }