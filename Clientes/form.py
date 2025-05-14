from django import forms
from .models import ClientePadre


class ClientePadreForm(forms.ModelForm):
    class Meta:
        model = ClientePadre
        fields = ['nombre', 'primerApellido', 'SegundoApellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'primerApellido': forms.TextInput(attrs={'class': 'form-control'}),
            'SegundoApellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }   