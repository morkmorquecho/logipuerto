from django.contrib import admin

from .models import SolicitudIndividual, SolicitudMasiva, TipoSegregacion  # Importa tus modelos aquí

# Registra tus modelos en el administrador
@admin.register(TipoSegregacion)
class Modelo1Admin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'grupo', 'tipo_operacion', 'tipo_servicio', 'fecha_creacion')
    search_fields = ('nombre', 'grupo', 'tipo_operacion', 'tipo_servicio__nombre')
    list_filter = ('grupo', 'tipo_operacion', 'tipo_servicio')
    ordering = ('-fecha_creacion',)
    

@admin.register(SolicitudMasiva)
class Modelo2Admin(admin.ModelAdmin):
    list_display = ('tipo_segregacion', 'user', 'cliente_hijo', 'cliente_padre', 'servicio', 'fecha_creacion')
    search_fields = ('tipo_segregacion__nombre', 'user__username', 'cliente_hijo__nombre', 'cliente_padre__razon_social')
    list_filter = ('tipo_segregacion', 'servicio', 'fecha_creacion')

@admin.register(SolicitudIndividual)
class SolicitudIndividualAdmin(admin.ModelAdmin):
    list_display = ('id_contenedor', 'solicitud_masiva', 'estado', 'bl', 'contenedor', 'fecha_creacion')
    search_fields = ('id_contenedor', 'bl', 'contenedor')
    list_filter = ('estado', 'fecha_creacion')