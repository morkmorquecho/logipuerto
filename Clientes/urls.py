from django.urls import path
from .wizard_views import FORMS
from .views import ListaClientesPadreView, DetalleClientePadreView, ListaClientesHijoView, editar_cliente, exportar_clientes_padres_excel, manejo_vdv, ListaClientePadreVDV_View
from .wizard_views import CrearClientePadreWizardView

clientes_patterns = ([
    # Clientes Padre
    path('clientes-padre/', ListaClientesPadreView.as_view(), name='clientes_padre_lista'),
    path('clientes-padre/crear/', CrearClientePadreWizardView.as_view(FORMS), name='clientes_padre_crear'),
    path('clientes-padre/<int:pk>/', DetalleClientePadreView.as_view(), name='clientes_padre_detalle'),
    path('clientes-padre/<int:pk>/editar/', editar_cliente, name='clientes_padre_editar'),
    path('clientes-padre/exportar/excel/', exportar_clientes_padres_excel, name='clientes_padre_exportar_excel'),
    
    # Clientes Hijo
    path('clientes-hijos/<int:pk>/', ListaClientesHijoView.as_view(), name='clientes_hijos_lista'),
    
    # VDV - Validador Digito Verificador
    path('clientes-padre/<int:pk>/vdv/', manejo_vdv, name='clientes_padre_manejo_vdv'),
    path('clientes-padre/vdv/', ListaClientePadreVDV_View.as_view(), name='clientes_padre_vdv_lista'),
], 'clientes')
