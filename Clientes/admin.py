from django.contrib import admin
from .models import *
from django_countries.widgets import CountrySelectWidget



@admin.register(TipoDeServicio)
class TipoDeServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'descripcion')
    search_fields = ('servicio', 'descripcion')

@admin.register(ClientePadre)
class ClientePadreAdmin(admin.ModelAdmin):
    list_display = ('id', 'razon_social', 'rfc', 'user', 'fecha_creacion')
    list_filter = ('regimen_fiscal', 'usoCFDI')
    search_fields = ('razon_social', 'rfc')
    raw_id_fields = ('user',)
    date_hierarchy = 'fecha_creacion'
    
    # Habilitar acciones incluyendo delete
    actions = ['delete_selected', 'custom_delete_action']
    
    # Mostrar el botón de eliminar en la vista de cambio
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' not in actions:
            actions['delete_selected'] = (
                self.get_action('delete_selected'),
                'delete_selected',
                'Eliminar seleccionados'
            )
        return actions
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('user', 'razon_social', 'rfc', 'tipo_rfc')
        }),
        ('Dirección', {
            'fields': ('pais', 'estado', 'ciudad', 'colonia', 'localidad', 
                      'codigo_postal', 'calle', 'numero_exterior', 'numero_interior')
        }),
        ('Datos Fiscales', {
            'fields': ('usoCFDI', 'regimen_fiscal',
                     'tipo_de_servicio')
        }),
    )

    formfield_overrides = {
        CountryField: {'widget': CountrySelectWidget(attrs={
            'class': 'form-control',
            'style': 'width: 300px;'
        })}
    }
    
    


@admin.register(ClienteHijo)
class ClienteHijoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cliente_padre', 'fecha_creacion')
    list_filter = ('cliente_padre',)
    search_fields = ('user__username', 'cliente_padre__razon_social')
    raw_id_fields = ('user', 'cliente_padre')

@admin.register(ContactoClientePadre)
class ContactoClientePadreAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_padre', 'nombre', 'correo', 'movil')
    search_fields = ('nombre', 'correo', 'cliente_padre__razon_social')
    raw_id_fields = ('cliente_padre',)

@admin.register(Documentos)
class DocumentosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente_padre', 'constancia_fiscal', 'contrato')
    search_fields = ('cliente_padre__razon_social', 'constancia_fiscal')
    raw_id_fields = ('cliente_padre',)