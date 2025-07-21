from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.utils import timezone


class UsoCFDI(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True, verbose_name="Código",default=1)
    descripcion = models.TextField(verbose_name="Descripción", default=1)
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class RegimenFiscal(models.Model):
    codigo = models.IntegerField(verbose_name="Código")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción", default="Por definir")
    
    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class RegistroBase(models.Model):
    TIPO_RFC_CHOICES = [
        ('FISICA', 'Persona Física'),
        ('MORAL', 'Persona Moral'),
        ('EXTRANJERO', 'Persona Extranjera'), ]


    rfc = models.CharField(max_length=20, verbose_name="RFC")
    tipo_rfc = models.CharField(max_length=50, verbose_name="Tipo RFC", choices=TIPO_RFC_CHOICES)
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    pais = CountryField(blank_label='(Seleccione país)', default="MX")
    estado = models.CharField(max_length=100, verbose_name="Estado")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    colonia = models.CharField(max_length=100, verbose_name="Colonia")
    localidad = models.CharField(max_length=100, blank=True, null=True, verbose_name="Localidad")
    codigo_postal = models.IntegerField(verbose_name="Código Postal")
    calle = models.CharField(max_length=255, verbose_name="Calle")
    numero_exterior = models.IntegerField(verbose_name="Número Exterior", default=0)
    numero_interior = models.IntegerField(blank=True, null=True, verbose_name="Número Interior")
    usoCFDI = models.ForeignKey(UsoCFDI, on_delete=models.PROTECT, verbose_name="Uso CFDI", null=True, blank=True)
    regimen_fiscal = models.ForeignKey(RegimenFiscal, on_delete=models.PROTECT, verbose_name="Régimen Fiscal", null=True, blank=True)
    referencia = models.TextField(blank=True, null=True, verbose_name="Referencia")
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name="Fecha de creación")
    class Meta:
        abstract = True

    def __str__(self):
        return self.razon_social
    
class ContactoBase(models.Model):
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    movil = models.CharField(max_length=20, verbose_name="Móvil")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    notas = models.TextField(verbose_name="Notas", blank=True, null=True)
    correo = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    
    def __str__(self):
        return f"Contacto de {self.nombre or 'Sin Nombre'}"
    class Meta:
        abstract = True