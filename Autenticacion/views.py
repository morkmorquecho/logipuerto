from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect

from Core.mixins import MessageMixin

class CustomLoginView(LoginView, MessageMixin):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        mensaje = "Nombre de usuario o contraseña incorrectos."
        self.error(mensaje)
        return super().form_invalid(form)

    def form_valid(self, form):
        return redirect('inicio')  # Asegúrate de que 'inicio' esté definido en tus URLs