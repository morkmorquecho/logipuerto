from django.db import models
from django.contrib.auth.models import User
from Core.models import ContactoBase, RegistroBase
from django.core.validators import FileExtensionValidator

class AgenciaAduanal(RegistroBase):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario", related_name="usuario_agencia_aduanal")
    cliente_padre = models.ManyToManyField('Clientes.ClientePadre', verbose_name="Cliente Padre", related_name="agencias_aduanales")

    def __str__(self):
        return f"{self.razon_social}"


class AgenteAduanal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario", related_name="usuario_agente_aduanal")
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la Agencia Aduanal", blank=True, null=True)
    correo = models.EmailField(verbose_name="Correo Electrónico", blank=True, null=True)
    patente = models.CharField(max_length=20, verbose_name="Patente Aduanal", unique=True, blank=True, null=True)
    agencia_aduanal = models.ForeignKey(AgenciaAduanal, on_delete=models.CASCADE, verbose_name="Agencia Aduanal", related_name="agentes_aduanales", blank=True, null=True)

    def __str__(self):
        return self.nombre


class ContactoAgenciaAduanal(ContactoBase):
    agencia_aduanal = models.OneToOneField(AgenciaAduanal, on_delete=models.CASCADE, verbose_name="Agente Aduanal", related_name="contacto_agencia_aduanal")

    def __str__(self):
        return f"Contacto de {self.agencia_aduanal.razon_social}"
    

def documentos_cliente_upload_to(instance, filename):
    """Guarda archivos en: agentesAduanales/[razon_social]/[filename]"""
    return f'Agencias Aduanales/{instance.agencia_aduanal.razon_social}/{filename}'

class DocumentosAgenciaAduanal(models.Model):
    agencia_aduanal = models.OneToOneField(AgenciaAduanal, on_delete=models.CASCADE, verbose_name="Cliente Padre")
    constancia_fiscal =  models.FileField( upload_to=documentos_cliente_upload_to, verbose_name="Constancia Fiscal (PDF)", validators=[FileExtensionValidator(allowed_extensions=['pdf'])] )
    
    def delete(self, *args, **kwargs):
        """Borrar archivos físicos cuando se elimina el registro"""
        if self.constancia_fiscal:
            self.constancia_fiscal.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return f"Documentos de {self.agencia_aduanal.razon_social}"