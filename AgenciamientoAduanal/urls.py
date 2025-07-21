
from django.urls import path
from .wizard_views import FORMS

from AgenciamientoAduanal.views import SeleccionarAgenciaAduanalView  , ListaAgentesAduanalesView, ListaClientesPadreView__AA, ListaAgenciasAduanalesView,ListaAgentesAduanalesView__Admin, DetalleAgenciaAduanalView
from AgenciamientoAduanal.wizard_views import CrearAgeciaAduanalWizardView



agenciamiento_aduanal_patterns = ([
    #Agentes Aduanales
    path('agentes-aduanales/', ListaAgentesAduanalesView.as_view(), name="agentes_aduanales_lista" ),
    path('agencias-aduanales/crear/', CrearAgeciaAduanalWizardView.as_view(FORMS), name="agencias_aduanales_crear"),
    path('agentes-aduanales/<int:pk>/', ListaAgentesAduanalesView__Admin.as_view(), name="agentes_aduanales_lista__admin"),
    
    #Agencias Aduanales
    path('clientes-padre/<int:pk>/agencias-aduanales/escoger/', SeleccionarAgenciaAduanalView  .as_view(), name="clientes_padre_agencias_aduanales_escoger"),
    path('agencias-aduanales/clientes-padre/', ListaClientesPadreView__AA.as_view(), name="agencias_aduanales_clientes_padre_lista"),
    path('agencias-aduanales/', ListaAgenciasAduanalesView.as_view(), name="agencias_aduanales_lista"),
    path('agencias-aduanales/<int:pk>/detalle/', DetalleAgenciaAduanalView.as_view(), name="agencias_aduanales_detalle"),

], "agenciamiento_aduanal")
