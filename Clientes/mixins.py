from Clientes.models import ClientePadre, ClienteHijo

class ClienteRolMixin:
    def obtener_id_cliente_padre(self, user):
        """
        Retorna el ID del cliente padre asociado al usuario,
        ya sea directamente (si es cliente padre) o a través del cliente hijo.
        """
        cliente_padre = ClientePadre.objects.filter(user=user).first()
        if cliente_padre:
            return cliente_padre.id

        cliente_hijo = ClienteHijo.objects.filter(user=user).first()
        if cliente_hijo and cliente_hijo.cliente_padre:
            return cliente_hijo.cliente_padre.id

        return None
    
    def es_cliente_padre(self, user):
        """
        Verifica si el usuario es un cliente padre.
        """
        return ClientePadre.objects.filter(user=user).exists()
