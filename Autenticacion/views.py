from typing import Any
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist  
from django.forms import ValidationError
from django.views.generic import CreateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from AgenciamientoAduanal.models import AgenciaAduanal, AgenteAduanal
from Core.mixins import MessageMixin, PasswordResetEmailMixin
from Clientes.models import ClienteHijo, ClientePadre
from .form import AgenteUserCreationForm, AutoPasswordUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from Core.mixins import GroupRequiredMixin

class BaseRegisterView(GroupRequiredMixin, MessageMixin, CreateView):
    form_class = AutoPasswordUserCreationForm
    template_name = 'registration/register.html'
    
    
    def form_valid(self, form):
        self.object = form.save()
        
        if self.group_name:
            try:
                group = Group.objects.get(name=self.group_name)
                self.object.groups.add(group)  
            except Group.DoesNotExist:
                pass
        self.success(self.get_success_message())

        return super().form_valid(form)
    
    def form_invalid(self, form):
        error_messages = form.errors.as_text()
        self.error(error_messages)
        print("Formulario inválido:")
        print(form.errors.as_json())  # o form.errors.as_data() para más detalle
        print("Datos del formulario:")
        print(form.data)
    
        return super().form_invalid(form)

    def get_success_message(self):
        return ""  
    
    def get_error_message(self):

        return "" 
    
    
class RegistrarUserPadreView(BaseRegisterView):
    success_url = reverse_lazy('clientes:clientes_padre_crear')
    group_name = "ClientePadre"
    group_required = ["Logipuerto", "Administrador"]

    def form_valid(self, form):

        self.request.session['correo'] = form.cleaned_data.get('email')
        self.request.session['usuario'] = form.cleaned_data.get('username')
        
        return super().form_valid(form)

    
    def get_success_message(self):
        return "El cliente Padre se ha creado correctamente"
    
    def get_error_message(self):
        return "Error al crear el cliente Padre, estás utilizando un nombre de NombreUsuario existente"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["titulo"] = "Crea el usuario del Cliente Padre"
            return context

class RegistrarUserHijoView(BaseRegisterView, PasswordResetEmailMixin):
    success_url = reverse_lazy('core:inicio')
    group_name = "ClienteHijo"
    email_template_name = 'registration/password_reset_email.html'
    group_required = ["ClientePadre"]

    def form_valid(self, form):
        cliente_padre = get_object_or_404(ClientePadre, user_id=self.request.user)        
        cantidadHijos = ClienteHijo.objects.filter(cliente_padre=cliente_padre).count()

        if cantidadHijos >= 3:
            self.error_message = "Límite alcanzado: No puedes registrar más de 3 clientes hijos"
            form.add_error(None, self.error_message)
            return self.form_invalid(form)

        response = super().form_valid(form)
        
        # Primero crea el hijo sin los servicios
        nuevo_hijo = ClienteHijo.objects.create(
            user=self.object,
            cliente_padre=cliente_padre,
        )
        
        # Luego establece la relación ManyToMany
        nuevo_hijo.servicios.set(cliente_padre.servicios.all())

        # Enviar correo al usuario para el restablecimiento de contraseña
        correo = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        self.enviar_password_reset_email(correo, username, True)
        
        return response

    def get_error_message(self):
        return getattr(self, 'error_message', "Error al crear el cliente Hijo")
    
    def get_success_message(self):
        return "El Usuario del cliente se ha creado correctamente, verifica tu correo para establecer la contraseña"
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["titulo"] = "Crea tu Usuario Hijo"
            return context
class RegistrarUserHijoView_Admin(BaseRegisterView, PasswordResetEmailMixin):
    success_url = reverse_lazy('core:inicio')
    group_name = "ClienteHijo"
    email_template_name = 'registration/password_reset_email.html'
    group_required = ["Logipuerto", "Administrador"]

    def form_valid(self, form):
        response = super().form_valid(form)

        cliente_padre_id = self.kwargs.get('pk')
        cliente_padre = get_object_or_404(ClientePadre, id=cliente_padre_id)
        servicios = cliente_padre.servicios

        nuevo_hijo = ClienteHijo.objects.create(
            user=self.object,
            cliente_padre=cliente_padre,
        )

        nuevo_hijo.servicios.set(servicios.all())

        correo = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        self.enviar_password_reset_email(correo,username,True)
        
        return response

    def get_error_message(self):
        return getattr(self, 'error_message', "Error al crear el cliente Hijo")
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crea un Cliente Hijo"
        return context

    def get_success_message(self):
            return "El cliente Padre se ha creado correctamente, el correo para establecer la contraseña fue enviado"

class RegistrarUserAgenteView(BaseRegisterView, PasswordResetEmailMixin):
    form_class = AgenteUserCreationForm
    success_url = reverse_lazy('core:inicio')
    email_template_name = 'registration/password_reset_email.html'
    group_name = "AgenteAduanal"
    group_required = ["AgenciaAduanal", "Administrador"]

    def form_valid(self, form):
        response = super().form_valid(form)
        correo = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        patente = form.cleaned_data.get('patente')
        nombre = form.cleaned_data.get('nombre')

        self.enviar_password_reset_email(correo,username,True)

        AgenteAduanal.objects.create(
            user=self.object,
            nombre=nombre,
            correo=correo,
            patente=patente,
            agencia_aduanal=self.request.user.usuario_agencia_aduanal
        )

        return response
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Crea un Agente Aduanal"
        return context
    
    def get_success_message(self):
            return "El Agente se ha creado correctamente, el correo para establecer la contraseña fue enviado"
class RegistrarUserAgenciaView(BaseRegisterView, PasswordResetEmailMixin):
    success_url = reverse_lazy('agenciamiento_aduanal:agencias_aduanales_crear')
    email_template_name = 'registration/password_reset_email.html'
    group_name = "AgenciaAduanal"
    group_required = ["Logipuerto", "Administrador"]

    def form_valid(self, form):

        self.request.session['correo'] = form.cleaned_data.get('email')
        self.request.session['usuario'] = form.cleaned_data.get('username')
        
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["titulo"] = "Crea el usuario de la Agencia Aduanal"
            return context

    def get_success_message(self):
            return "El usuario de la Agencia se ha creado correctamente, el correo para establecer la contraseña fue enviado"
    
    def get_error_message(self):
        return "Error al crear la Agencia Aduanal"

class EliminarUsuarioView(GroupRequiredMixin,DeleteView):
    model = User 
    success_url = reverse_lazy('clientes:clientes_padre_lista')
    template_name = "User_confirm_delete.html"
    group_required = ["Logipuerto", "Administrador"]

def cambiar_estado_is_active(request, user_id):
    # if not request.user.is_staff:  
    #     return redirect('core:inicio')
    
    user = get_object_or_404(User, id=user_id)
    nuevo_estado = not user.is_active 
    user.is_active = nuevo_estado
    user.save()
    
    if ClientePadre.objects.filter(user=user).exists(): 
        cliente_padre = get_object_or_404(ClientePadre, user=user)
        usuarios_hijos = User.objects.filter(usuario_cliente_hijo__cliente_padre=cliente_padre)
        usuarios_hijos.update(is_active=nuevo_estado)

    
    return redirect(request.META.get('HTTP_REFERER', 'clientes:clientes_padre_detalle'))

class UsuariosBloqueadosView(GroupRequiredMixin,ListView):        
    model = User
    context_object_name = 'listadoUsuariosBloqueadosView'
    paginate_by = 20  
    template_name = "registration/UserLocked_list.html"
    # ordering = ['-fecha_creacion']
    group_required = ["Logipuerto", "Administrador"]
    raise_exception = True

    
    def get_queryset(self):
        return User.objects.filter(
                        is_active=False,
                        id__in=ClientePadre.objects.all().values('user')
                    )


