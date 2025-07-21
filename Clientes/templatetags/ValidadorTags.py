from django import template
from django.apps import apps
from Clientes.models import ClientePadre

register = template.Library()

@register.simple_tag
def estado_validador(pk):
    """
    Devuelve el estado del validador
    """
    validador = ClientePadre.objects.filter(pk=pk).first()
    return validador.digito_verificador if validador else False