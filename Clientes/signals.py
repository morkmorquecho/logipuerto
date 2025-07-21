import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Documentos

@receiver(pre_save, sender=Documentos)
def eliminar_archivo_anterior(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field_name in ['constancia_fiscal', 'contrato']:
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

@receiver(post_delete, sender=Documentos)
def eliminar_archivo_al_borrar(sender, instance, **kwargs):
    for field_name in ['constancia_fiscal', 'contrato']:
        archivo = getattr(instance, field_name)
        if archivo and os.path.isfile(archivo.path):
            os.remove(archivo.path)
