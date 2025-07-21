from django import forms
from Solicitudes.models import SolicitudMasiva, TipoSegregacion

class TipoSegregacionForm(forms.ModelForm):
    class Meta:
        model = TipoSegregacion
        fields = ['nombre', 'descripcion', 'grupo', 'tipo_operacion', 'tipo_servicio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'grupo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_operacion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),

        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'grupo': 'Grupo',
            'tipo_operacion': 'Tipo de Operación',
            'tipo_servicio': 'Tipo de Servicio',
        }



class SolicitudesMasivasBaseForm(forms.ModelForm):
    class Meta:
        model = SolicitudMasiva
        fields = ['tipo_segregacion', 'excel']
        widgets = {
            'tipo_segregacion': forms.Select(attrs={'class': 'form-control'}),
            'excel': forms.ClearableFileInput(attrs={'class': 'filepond', 
                                                     'accept': '.xlsx, .xls',
                'required': True
                }),
        }
        labels = {
            'tipo_segregacion': 'Tipo de Segregación',
            'excel': 'Archivo Excel',
        }