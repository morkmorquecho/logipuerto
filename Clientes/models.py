from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from Core.models import ContactoBase, RegistroBase
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save, pre_save


class TipoDeServicio(models.Model):
    servicio = models.CharField( max_length=100, verbose_name="Servicio")
    descripcion = models.TextField(verbose_name="Descripción")
    
    def __str__(self):
        return self.servicio

class ClientePadre(RegistroBase):

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario",  related_name="cliente_padre")
    servicios = models.ManyToManyField(TipoDeServicio,verbose_name="servicios")
    digito_verificador = models.BooleanField(default=True, verbose_name="Digito Verificador")
    def __str__(self):
        return self.razon_social


@receiver(post_save, sender=ClientePadre)
def actualizar_servicios_hijos(sender, instance, created, **kwargs):
    """
    Actualiza los servicios de todos los ClienteHijo cuando se modifican
    los servicios del ClientePadre
    """
    if not created:  # Solo en actualizaciones, no en creación
        # Obtener todos los servicios actuales del padre
        servicios_padre = instance.servicios.all()
        
        # Actualizar cada hijo
        for hijo in instance.hijos.all():
            hijo.servicios.clear()
            hijo.servicios.add(*servicios_padre)
            
            # Alternativa más eficiente para muchos registros:
            # hijo.servicios.set(servicios_padre)

class ClienteHijo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario", related_name="usuario_cliente_hijo")
    cliente_padre = models.ForeignKey(ClientePadre, on_delete=models.CASCADE, verbose_name="Cliente Padre", related_name="hijos")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    servicios = models.ManyToManyField(TipoDeServicio,verbose_name="servicios")
    
    def __str__(self):
        return f"{self.user.username} - {self.cliente_padre.razon_social}"

class ContactoClientePadre(ContactoBase):
    cliente_padre = models.OneToOneField(ClientePadre, on_delete=models.CASCADE, verbose_name="Cliente Padre")
    
    def __str__(self):
        return f"Contacto de {self.cliente_padre.razon_social}"


def documentos_cliente_upload_to(instance, filename):
    """Guarda archivos en: clientesPadres/[razon_social]/[filename]"""
    return f'Clientes/{instance.cliente_padre.razon_social}/Documentos de registro/{filename}'

class Documentos(models.Model):
    cliente_padre = models.OneToOneField(ClientePadre, on_delete=models.CASCADE, verbose_name="Cliente Padre")
    constancia_fiscal =  models.FileField( upload_to=documentos_cliente_upload_to, verbose_name="Constancia Fiscal (PDF)", validators=[FileExtensionValidator(allowed_extensions=['pdf'])] )
    contrato = models.FileField( upload_to=documentos_cliente_upload_to,verbose_name="contrato (PDF)", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def delete(self, *args, **kwargs):
        """Borrar archivos físicos cuando se elimina el registro"""
        if self.constancia_fiscal:
            self.constancia_fiscal.delete()
        if self.contrato:
            self.contrato.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"Documentos de {self.cliente_padre.razon_social}"



