from django import forms
from django.core.validators import RegexValidator
from AgenciamientoAduanal.models import AgenciaAduanal, AgenteAduanal, ContactoAgenciaAduanal, DocumentosAgenciaAduanal
from Clientes.models import ClientePadre
from django_countries.widgets import CountrySelectWidget


rfc_validator = RegexValidator(
        regex=r'^([A-ZÑ&]{3,4})\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[A-Z0-9]{3}$',
        message="Ingrese un RFC válido de persona física (4 letras, 6 dígitos de fecha, 3 caracteres alfanuméricos).",
        code="invalid_rfc"
    )

      
class ClientePadreEscogeAgenciaForm(forms.ModelForm):
    agencias = forms.ModelMultipleChoiceField(
        queryset=AgenciaAduanal.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2-multiple',
            'data-placeholder': 'Selecciona la agencia...',
        }),
        required=False
    )

    class Meta:
        model = ClientePadre  # Aquí editas ClientePadre
        fields = []  # No hace falta campos extras aquí

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-cargar agencias ya relacionadas con el cliente
            self.fields['agencias'].initial = self.instance.agencias_aduanales.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Guardamos las agencias seleccionadas en el ManyToMany inverso
            instance.agencias_aduanales.set(self.cleaned_data['agencias'])
        return instance

#Datos generales    
class Pagina1Form(forms.ModelForm):
    class Meta:
        
        model = AgenciaAduanal
        fields = ['rfc', 'tipo_rfc', 'razon_social']
        widgets = {
            'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RFC'}),
            'tipo_rfc': forms.Select(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rfc'].validators.append(rfc_validator)  # Añade el validador aquí

#Ubicacion
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
        model = AgenciaAduanal
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

# Datos Fiscales
class Pagina3Form(forms.ModelForm):
    class Meta:
        model = AgenciaAduanal
        fields = ['usoCFDI', 'regimen_fiscal', 'referencia']
        widgets = {
            'usoCFDI': forms.Select(attrs={'class': 'form-control'}),
            'regimen_fiscal': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'usoCFDI': 'Uso CFDI',            
        }
        
#Contacto
class Pagina4Form(forms.ModelForm):
    class Meta:
        model = ContactoAgenciaAduanal
        fields = 'nombre', 'movil', 'telefono', 'notas'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'movil': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'movil': 'Móvil',
            'telefono': 'Teléfono',
        }

#Documentos
class Pagina5Form(forms.ModelForm):
    class Meta:
        model = DocumentosAgenciaAduanal
        fields = ['constancia_fiscal']  
        
        widgets = {
            'constancia_fiscal': forms.ClearableFileInput(attrs={
                'class': 'filepond',
                'accept': '.pdf'
            }),         
        }