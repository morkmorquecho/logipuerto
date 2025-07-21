from django.db import models

from AgenciamientoAduanal.models import AgenteAduanal
from Clientes.models import ClientePadre


class SolicitudMasivaTransporte(models.Model):
    agente_aduanal = models.ForeignKey(AgenteAduanal, on_delete=models.CASCADE, verbose_name=("Agente Aduanal"), related_name="solicitud_masiva_transporte_agente_aduanal", blank=True, null=True) 
    fecha_creacion = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Solicitud Masiva de {self.agente_aduanal.agencia_aduanal.razon_social} - {self.fecha_creacion.strftime('%Y-%m-%d')}"
    
# Create your models here.
class SoliciudIndividualTransporte(models.Model):
    TIPO_MATERIAL_CHOICES = [
        ("01", "Materia Prima"),
        ("02", "Materia Procesada"),
        ("03", "Materia Terminada (Producto terminado)"),
        ("04", "Materia para la industria manufacturera"),
        ("05", "Otra")]

    solicitud_masiva = models.ForeignKey(SolicitudMasivaTransporte, on_delete=models.CASCADE, verbose_name=("Solicitud Masiva"), related_name="solicitudes_individuales_transporte")

    contenedor = models.CharField(max_length=11)
    iniciales_equipo = models.CharField(max_length=10, null=True, blank=True) #4 digitos de contenedor
    numero_equipo = models.CharField(max_length=10, null=True, blank=True) #digito 5 a 10 del contenedor
    digito_control = models.CharField(max_length=1, null=True, blank=True) #ultimo digito del contenedor
    
    bl = models.CharField(max_length=16)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    longitud_equipo = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name = "longitud del equipo en pies") #en pies
    sello_1 = models.CharField(max_length=20, null=True, blank=True, verbose_name=("Sello 1"))
    sello_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name=("Sello 2"))
    sello_3 = models.CharField(max_length=20, null=True, blank=True, verbose_name=("Sello 3"))
    sello_4 = models.CharField(max_length=20, null=True, blank=True, verbose_name=("Sello 4"))
    clave_producto_sat = models.CharField(max_length=20, verbose_name=("Clave Producto SAT"))
    tipo_material = models.CharField(max_length=50, verbose_name=("Tipo de Material"), choices= TIPO_MATERIAL_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=("Cantidad"))
    descripcion_sat = models.TextField(null=True, blank=True, verbose_name=("Descripción"))
    peso_neto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=("Peso Neto"))
    terminal_carga = models.CharField(max_length=100, verbose_name=("Terminal de Carga"))
    terminal_destino = models.CharField(max_length=100, null=True, blank=True, verbose_name=("Terminal de Destino"))
    cliente_padre = models.ForeignKey(ClientePadre, on_delete=models.CASCADE, verbose_name=("Cliente Padre"), related_name="solicitudes_individuales_transporte_cliente_padre")
    patente = models.CharField(max_length=20, verbose_name=("Patente"))
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    eliminada = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.contenedor and len(self.contenedor) == 11:
            self.iniciales_equipo = self.contenedor[:4]
            self.numero_equipo = self.contenedor[4:10]
            self.digito_control = self.contenedor[10]
        else:
            self.iniciales_equipo = None
            self.numero_equipo = None
            self.digito_control = None
        
        super().save(*args, **kwargs)