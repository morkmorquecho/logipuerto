from django import template
from django import template
from django.contrib.auth.models import User
from Clientes.models import ClienteHijo, ClientePadre, TipoDeServicio

register = template.Library()

#Te permite verificar la existencia de un usuario en un grupo solicitado
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


#Te permite verificar con cuales servicios cuenta el cliente

@register.filter(name='tiene_servicio')
def tiene_servicio(user_id, servicio_nombre):
    """
    Filtro para verificar si un usuario tiene un servicio.
    Uso: {% if user.id|tiene_servicio:"Ferrocarril directo" %}
    """
    cliente = None
    try:
        cliente = ClienteHijo.objects.filter(user_id=user_id).first()
        if not cliente:
            cliente = ClientePadre.objects.filter(user_id=user_id).first()

        if cliente:
            return cliente.servicios.filter(servicio=servicio_nombre).exists()
    except Exception:
        pass

    return False