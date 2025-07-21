from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(AgenciaAduanal)
class AgenciaAduanalAdmin(admin.ModelAdmin):
    list_display = ('id', 'razon_social', 'rfc', 'user', 'fecha_creacion')
    list_filter = ('regimen_fiscal', 'usoCFDI')
    search_fields = ('razon_social', 'rfc')
    raw_id_fields = ('user',)
    date_hierarchy = 'fecha_creacion'

@admin.register(AgenteAduanal)
class AgenteAduanalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'patente', 'agencia_aduanal')
    search_fields = ('nombre', 'correo', 'patente')
    raw_id_fields = ('agencia_aduanal',)
    list_filter = ('agencia_aduanal',)

@admin.register(ContactoAgenciaAduanal)
class ContactoAgenciaAduanalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono', 'agencia_aduanal')
    search_fields = ('nombre', 'correo', 'telefono')
    raw_id_fields = ('agencia_aduanal',)

@admin.register(DocumentosAgenciaAduanal)
class DocumentosAgenciaAduanalAdmin(admin.ModelAdmin):
    list_display = ('id', 'agencia_aduanal', 'constancia_fiscal')
    raw_id_fields = ('agencia_aduanal',)
