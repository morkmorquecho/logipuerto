from django.db import models

# Create your models here.
class ClientePadre(models.Model):
    nombre = models.CharField(max_length=100)
    primerApellido = models.CharField(max_length=100)
    SegundoApellido = models.CharField(max_length=100)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
