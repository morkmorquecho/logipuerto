from typing import Any
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.models import User

from AgenciamientoAduanal.forms import ClientePadreEscogeAgenciaForm
from AgenciamientoAduanal.models import AgenciaAduanal, AgenteAduanal
from Clientes.models import ClientePadre
from Core.mixins import GroupRequiredMixin


#ClientePadre escoge a sus agencias aduanales en esta vista
class SeleccionarAgenciaAduanalView(GroupRequiredMixin, UpdateView):
    model = ClientePadre
    form_class = ClientePadreEscogeAgenciaForm
    success_url = reverse_lazy('core:inicio')
    group_required = 'ClientePadre'
    template_name = 'AgenciamientoAduanal/form.html'

    def get_object(self, queryset=None):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        if not hasattr(user, "cliente_padre"):
            raise Http404("Este usuario no tiene ClientePadre asignado")
        return user.cliente_padre

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Escoge la agencia aduanal"
        context["accion"] = "Guardar"
        return context

class ListaAgentesAduanalesView(GroupRequiredMixin, ListView):
    model = AgenteAduanal
    context_object_name = 'agentes_aduanales'
    group_required = 'AgenciaAduanal'
    template_name = 'AgenciamientoAduanal/AgenteAduanal_listpro.html'

    def get_queryset(self):
        return super().get_queryset().filter(agencia_aduanal=self.request.user.usuario_agencia_aduanal)
    
class ListaClientesPadreView__AA(GroupRequiredMixin, ListView):
    model = ClientePadre
    context_object_name = 'clientes'
    group_required = 'AgenciaAduanal'
    template_name = 'AgenciamientoAduanal/ClientePadre_list.html'

    def get_queryset(self):
        return ClientePadre.objects.filter(agencias_aduanales=self.request.user.usuario_agencia_aduanal)
    
class ListaAgenciasAduanalesView(GroupRequiredMixin, ListView):
    model = AgenciaAduanal
    context_object_name = 'agencias_aduanales'
    group_required = 'Logipuerto'
    template_name = 'AgenciamientoAduanal/AgenciaAduanal_list.html'

class ListaAgentesAduanalesView__Admin(GroupRequiredMixin, ListView):
    model = AgenteAduanal
    context_object_name = 'agentes_aduanales'
    group_required = 'Logipuerto'
    template_name = 'AgenciamientoAduanal/AgenteAduanal_listpro.html'

    def get_queryset(self):
        return super().get_queryset().filter(agencia_aduanal=self.kwargs.get('pk'))

class DetalleAgenciaAduanalView(GroupRequiredMixin, DetailView):
    model = AgenciaAduanal
    context_object_name = 'agencia_aduanal'
    group_required = 'Logipuerto'
    template_name = 'AgenciamientoAduanal/AgenciaAduanal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['contacto'] = self.object.contacto_agencia_aduanal
        context['documentos'] = self.object.documentosagenciaaduanal
        return context