from django.urls import path
from . import views
from .views import CrearClientePadre
clientes_patterns =( [
    path('CrearClientePadre/', CrearClientePadre.as_view(), name='clientePadre'),
], 'clientes')