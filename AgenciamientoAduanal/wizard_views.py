from formtools.wizard.views import SessionWizardView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from .forms import Pagina1Form, Pagina2Form, Pagina3Form, Pagina4Form, Pagina5Form
from django.core.files.storage import FileSystemStorage
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from .models import AgenciaAduanal, ContactoAgenciaAduanal, DocumentosAgenciaAduanal
from Core.mixins import GroupRequiredMixin, MessageMixin, PasswordResetEmailMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

FORMS = [
    ("informacion_general", Pagina1Form),
    ("direccion", Pagina2Form),
    ("datos_fiscales", Pagina3Form),
    ("datos_contacto", Pagina4Form),
    ("documentos", Pagina5Form),
]

TEMPLATES = {
    "informacion_general": "Clientes/clientePadre_wizard_pagina1.html",
    "direccion": "Clientes/clientePadre_wizard_pagina2.html",
    "datos_fiscales": "Clientes/clientePadre_wizard_pagina3.html",
    "datos_contacto": "Clientes/clientePadre_wizard_pagina4.html",
    "documentos": "Clientes/clientePadre_wizard_pagina5.html",
}

class CrearAgeciaAduanalWizardView(GroupRequiredMixin,PasswordResetEmailMixin, MessageMixin,PasswordResetView, SessionWizardView):
    group_required = 'Logipuerto'  
    #el contenido del correo que se enviara al usuario
    email_template_name = 'registration/password_reset_email.html'

    file_storage = FileSystemStorage(
        location=settings.MEDIA_ROOT,  
        base_url=settings.MEDIA_URL   
    )

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        with transaction.atomic():
            try:

                forms_dict = {form.prefix: form for form in form_list}
                
                correo = self.request.session.get('correo')

                #obtener la instancia del usuario a partir del nombre del usuario proporcionado de RegistrarUserAgenciaView
                try:
                    username = self.request.session.get('usuario')  # Misma clave que en RegistrarUserAgenciaView
                    usuario = User.objects.get(username=username)  # Obtener el User completo
                except User.DoesNotExist:
                    raise ValueError(f"Usuario con username '{username}' no existe")

                # Combinar datos de los formularios
                agencia_data = {
                    **forms_dict['informacion_general'].cleaned_data,
                    **forms_dict['direccion'].cleaned_data,
                    **forms_dict['datos_fiscales'].cleaned_data
                }

                # Crear el objeto AgenciaAduanal 
                agencia_aduanal = AgenciaAduanal.objects.create(
                    user=usuario,
                    **agencia_data)
       
                ContactoAgenciaAduanal.objects.create(
                    agencia_aduanal=agencia_aduanal, 
                    correo=correo,
                    **forms_dict['datos_contacto'].cleaned_data
                )
                
                
                if 'documentos' in forms_dict and forms_dict['documentos'].cleaned_data:
                    DocumentosAgenciaAduanal.objects.create(
                        agencia_aduanal=agencia_aduanal,  # Usar la instancia creada
                        **forms_dict['documentos'].cleaned_data
                    )


                #Instanciar del form que restablece contraseñas
                #Seccion que envia link de restablecimiento de contraseña al usuario
                self.enviar_password_reset_email(correo, username, welcome=True)
                
                # Limpiar sesión
                if 'NombreUsuario' in self.request.session:
                    del self.request.session['NombreUsuario']
                if 'correo' in self.request.session:
                    del self.request.session['correo']

                self.success("Se ha creado el agencia correctamente")
                return redirect(reverse_lazy('core:inicio'))
            
            except Exception as e:
                self.error(f"Error al crear el agencia: {str(e)}")
                return redirect(reverse_lazy('core:inicio'))

        
