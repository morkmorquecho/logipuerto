from django import forms
from AgenciamientoAduanal.models import AgenteAduanal
from Ferrocarril.models import SoliciudIndividualTransporte
from Solicitudes.models import SolicitudMasiva, TipoSegregacion
from Solicitudes.form import SolicitudesMasivasBaseForm

class SolicitudesMasivasFerroForm(SolicitudesMasivasBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_segregacion'].queryset = TipoSegregacion.objects.filter(tipo_servicio_id=1)

class BuscarContenedoresPorBLForm(forms.Form):
    bl = forms.CharField(
        label="BL",
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el BL de los contenedores que necesita'})
    )


class CrearSolicitudesTransporteForm(forms.ModelForm):
    patente = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        model = SoliciudIndividualTransporte
        fields = ['clave_producto_sat', 'tipo_material', 'cantidad', 'patente']
        # widgets = {
        #     'clave_producto_sat': forms.TextInput(attrs={'class': 'form-input', 'placeholder' : 'Ingresa la clave del producto'}),
        #     'cantidad': forms.TextInput(attrs={'class': 'form-input', 'placeholder' : 'Ingresa el Numero de bultos de la carga'}),
        #     'tipo_material': forms.Select(attrs={'class': 'form-select', 'placeholder' :'Selecciona el tipo de material'}),
        # }

        widgets = {
            'clave_producto_sat': forms.TextInput(attrs={
                'class': 'form-input clave-producto-input',  # Agregamos la clase aquí
                'placeholder': 'Ingresa la clave del producto'
            }),
            'cantidad': forms.TextInput(attrs={
                'class': 'form-input', 
                'placeholder': 'Ingresa el Numero de bultos de la carga'
            }),
            'tipo_material': forms.Select(attrs={
                'class': 'form-select', 
                'placeholder': 'Selecciona el tipo de material'
            }),
        }

    def __init__(self, *args, **kwargs):
        usuario_agente = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

        if usuario_agente:
            agencia_aduanal = usuario_agente.usuario_agente_aduanal.agencia_aduanal

            # Obtener patentes como lista de tuplas (valor, etiqueta)
            patentes = AgenteAduanal.objects.filter(
                agencia_aduanal=agencia_aduanal,
                patente__isnull=False
            ).values_list('patente', 'patente')

            self.fields['patente'].choices = patentes