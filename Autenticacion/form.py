# forms.py
from django.contrib.auth.models import User
import secrets  
import string
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm

class AutoPasswordUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['username'].help_text = "El nombre de usuario debe ser su correo antes del @ ejemplo: CLopez@contecon.mx - CLopez"

    def clean_password2(self):
        # Bypass password validation
        return self.cleaned_data.get("password1")

    def save(self, commit=True):
        user = super().save(commit=False)
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        print(f"----------------------------Generated password: {password}")
        user.set_password(password)
        if commit:
            user.save()
        return user

class AgenteUserCreationForm(AutoPasswordUserCreationForm):
    patente = forms.CharField(max_length=20, required=True, label="Patente")
    nombre = forms.CharField(max_length=50, required=True, label="Nombre del Agente Aduanal")
    
    class Meta(AutoPasswordUserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que los campos adicionales estén disponibles
        self.fields['patente'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
    

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico'
        })
