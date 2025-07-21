from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from AgenciamientoAduanal.models import AgenteAduanal
from Clientes.models import ClienteHijo, ClientePadre, TipoDeServicio

# Create your models here.
class TipoSegregacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    grupo = models.CharField(max_length=50)
    tipo_operacion = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)    
    tipo_servicio = models.ForeignKey(TipoDeServicio, on_delete=models.PROTECT,verbose_name=("Tipo de Servicio"))

    def __str__(self):
        return self.nombre

def documentos_cliente_upload_to(instance, filename):
    
    """Guarda archivos en: Clientes/[username]/solicitudes/Ferro/fecha/"""
    return f'Clientes/{instance.cliente_padre.razon_social}/Solicitudes/Ferro/{date.today()}/{filename}'

class SolicitudMasiva(models.Model):
    tipo_segregacion = models.ForeignKey(TipoSegregacion, on_delete=models.CASCADE, verbose_name=("Tipo de Segregación"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("Usuario"))
    cliente_hijo = models.ForeignKey(ClienteHijo, on_delete=models.CASCADE, verbose_name=("Cliente Hijo"), blank = True, null = True)
    cliente_padre = models.ForeignKey(ClientePadre,on_delete=models.CASCADE, verbose_name=("Cliente Padre"), blank = True, null = True )
    servicio = models.ForeignKey(TipoDeServicio, on_delete=models.CASCADE, verbose_name=("Servicio"))
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    excel = models.FileField( upload_to=documentos_cliente_upload_to,verbose_name="contrato (PDF)", validators=[FileExtensionValidator(allowed_extensions=['xlsx','csv'])])

    def delete(self, *args, **kwargs):
        """Borrar archivos físicos cuando se elimina el registro"""
        if self.excel:
            self.excel.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Solicitud Masiva de {self.cliente_padre.razon_social} - {self.fecha_creacion.strftime('%Y-%m-%d')}"

class SolicitudIndividual(models.Model):
    id_contenedor = models.CharField(max_length=20, null=True, blank=True, verbose_name=("ID Contenedor"))
    solicitud_masiva = models.ForeignKey(SolicitudMasiva, on_delete=models.CASCADE, verbose_name=("Cita Masiva"), related_name="solicitudes_individuales")
    estado = models.CharField(max_length=50, default='Nueva')
    estatus_n4 = models.CharField(max_length=50, default='Nueva')
    bl = models.CharField(max_length=16)
    tipo_tamaño = models.CharField(max_length=5,null=True, blank=True)
    contenedor = models.CharField(max_length=11)
    viaje = models.CharField(max_length=17, null=True, blank=True)
    buque = models.CharField(max_length=35,null=True, blank=True)
    eta = models.DateTimeField( null=True, blank=True)
    imo = models.BooleanField(null=True, blank=True)
    esReefer = models.BooleanField(null=True, blank=True)
    isOOG = models.BooleanField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    destino = models.CharField(max_length=100, null=True, blank=True)
    eliminada = models.BooleanField(default = False)

