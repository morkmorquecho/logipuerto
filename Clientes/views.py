from django.shortcuts import render
from django.views.generic import CreateView

from .form import ClientePadreForm
from .models import ClientePadre

# Create your views here.
class CrearClientePadre(CreateView):
    model = ClientePadre
    form_class = ClientePadreForm
    