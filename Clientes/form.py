from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import ClientePadre, ClienteHijo, ContactoClientePadre, Documentos
from formtools.wizard.views import SessionWizardView
from django_countries.widgets import CountrySelectWidget
from django.core.validators import FileExtensionValidator
from django.forms import ClearableFileInput

rfc_validator = RegexValidator(
        regex=r'^([A-ZÑ&]{3,4})\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[A-Z0-9]{3}$',
        message="Ingrese un RFC válido de persona física (4 letras, 6 dígitos de fecha, 3 caracteres alfanuméricos).",
        code="invalid_rfc"
    )

#Se uso wizard para crear un formulario de varios pasos, por ello el nombre de las clases, pero en model puedes ver la referencia al modelo que sera afectado
class Pagina1Form(forms.ModelForm):
    class Meta:
        
        model = ClientePadre
        fields = ['rfc', 'tipo_rfc', 'razon_social']
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RFC'}),
            'tipo_rfc': forms.Select(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rfc'].validators.append(rfc_validator)  # Añade el validador aquí

class Pagina2Form(forms.ModelForm):

    ESTADOS_MEXICO = [
    ("Aguascalientes", "Aguascalientes"),
    ("Baja California", "Baja California"),
    ("Baja California Sur", "Baja California Sur"),
    ("Campeche", "Campeche"),
    ("Ciudad de México", "Ciudad de México"),
    ("Chiapas", "Chiapas"),
    ("Chihuahua", "Chihuahua"),
    ("Coahuila", "Coahuila"),
    ("Colima", "Colima"),
    ("Durango", "Durango"),
    ("Guanajuato", "Guanajuato"),
    ("Guerrero", "Guerrero"),
    ("Hidalgo", "Hidalgo"),
    ("Jalisco", "Jalisco"),
    ("Estado de México", "Estado de México"),
    ("Michoacán", "Michoacán"),
    ("Morelos", "Morelos"),
    ("Nayarit", "Nayarit"),
    ("Nuevo León", "Nuevo León"),
    ("Oaxaca", "Oaxaca"),
    ("Puebla", "Puebla"),
    ("Querétaro", "Querétaro"),
    ("Quintana Roo", "Quintana Roo"),
    ("San Luis Potosí", "San Luis Potosí"),
    ("Sinaloa", "Sinaloa"),
    ("Sonora", "Sonora"),
    ("Tabasco", "Tabasco"),
    ("Tamaulipas", "Tamaulipas"),
    ("Tlaxcala", "Tlaxcala"),
    ("Veracruz", "Veracruz"),
    ("Yucatán", "Yucatán"),
    ("Zacatecas", "Zacatecas")
    ]
    
    estado = forms.ChoiceField(
        choices=ESTADOS_MEXICO,
        widget=forms.Select(attrs={'class': 'form-control select2-estado'})
    )
    
    class Meta:  
        model = ClientePadre
        fields = ['pais', 'estado', 'ciudad', 'colonia', 'localidad', 
                 'codigo_postal', 'calle', 'numero_exterior', 'numero_interior']
        widgets = {
            'pais': CountrySelectWidget(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'colonia': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.NumberInput(attrs={'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_exterior': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_interior': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'numero_exterior': 'Número exterior',
            'numero_interior': 'Número interior',
            'codigo_postal': 'Código Postal',
        }

class Pagina3Form(forms.ModelForm):
    class Meta:
        model = ClientePadre
        fields = ['usoCFDI', 'regimen_fiscal',  
                  'servicios', 'referencia']
        widgets = {
            'usoCFDI': forms.Select(attrs={'class': 'form-control'}),
            'regimen_fiscal': forms.Select(attrs={'class': 'form-control'}),
            'servicios': forms.CheckboxSelectMultiple(),
            'referencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'usoCFDI': 'Uso CFDI',            
        }
        
#Contacto
class Pagina4Form(forms.ModelForm):
    class Meta:
        model = ContactoClientePadre
        fields = 'nombre', 'movil', 'telefono', 'notas'
        widgets = {
            #'cliente_padre': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'movil': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            # 'cliente_padre': 'Cliente Padre',
            'movil': 'Móvil',
            'telefono': 'Teléfono',
        }


class Pagina5Form(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['constancia_fiscal', 'contrato']  # Nombres correctos de campos
        
        widgets = {
            'constancia_fiscal': forms.ClearableFileInput(attrs={
                'class': 'filepond',
                'accept': '.pdf'
            }),
            'contrato': forms.ClearableFileInput (attrs={
                'class': 'filepond',
                'accept': '.pdf'
            }),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.FileField):
                clases = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{clases} form-control"
                field.widget.attrs['accept'] = '.pdf'  
class ClienteHijoForm(forms.ModelForm):
    class Meta:
        model = ClienteHijo
        fields = ['user', 'cliente_padre']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'cliente_padre': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'Usuario asociado',
            'cliente_padre': 'Cliente Padre',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_active=True)

