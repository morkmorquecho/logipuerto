from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.db.models import Q
from Clientes.mixins import ClienteRolMixin
from Core.mixins import GroupRequiredMixin
from Clientes.models import ClienteHijo, ClientePadre, TipoDeServicio
from Solicitudes.form import TipoSegregacionForm
from Solicitudes.models import SolicitudIndividual, SolicitudMasiva, TipoSegregacion
from Ferrocarril.service import SegregarContenedores
# Create your views here.
class CrearTipoSegregacionView(GroupRequiredMixin, CreateView):
    model = TipoSegregacion
    form_class = TipoSegregacionForm
    success_url = reverse_lazy('core:inicio')
    group_required = 'Logipuerto'  

class ListaSolicitudesMasivasAdminView(GroupRequiredMixin, ListView):
    model = SolicitudMasiva
    template_name = "Solicitudes/SolicitudMasivasAdmin_list.html"
    context_object_name = 'solicitudes_masivas'
    paginate_by = 20  
    ordering = ['-fecha_creacion']
    group_required = 'Logipuerto'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha_creacion')
        search_query = self.request.GET.get('q')
        
        clientes = self.request.GET.get('clientes')
        if clientes:
            queryset = queryset.filter(cliente_hijo__cliente_padre__razon_social=clientes)

        segregacion = self.request.GET.get('segregacion')
        if segregacion:
            queryset = queryset.filter(tipo_segregacion__nombre=segregacion)

        servicio = self.request.GET.get('servicio')
        if servicio:
            queryset = queryset.filter(servicio__servicio=servicio)

        # Barra de búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(tipo_segregacion__nombre__icontains=search_query) |  
                Q(user__username__icontains=search_query) |
                Q(cliente_hijo__cliente_padre__razon_social__icontains=search_query) |
                Q(cliente_hijo__cliente_padre__rfc__icontains=search_query) |
                Q(fecha_creacion__icontains=search_query))  
    
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date() + timedelta(days=1) 
            
        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            queryset = queryset.filter(fecha_creacion__gte=fecha_inicio)
        elif fecha_fin:
            queryset = queryset.filter(fecha_creacion__lte=fecha_fin)

        return queryset

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['TiposDeServicios'] = TipoDeServicio.objects.all()
        context['TiposDeSegregacion'] = TipoSegregacion.objects.all()
        context['Clientes'] = ClientePadre.objects.all()
        return context
    
class ListaSolicitudesMasivasUserPadreView(ClienteRolMixin, GroupRequiredMixin, ListView):
    model = SolicitudMasiva
    template_name = "Solicitudes/SolicitudMasivasUserPadre_list.html"
    context_object_name = 'solicitudes_masivas'
    paginate_by = 20  
    ordering = ['-fecha_creacion']
    group_required = ['ClientePadre', 'ClienteHijo'] 
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha_creacion')
        search_query = self.request.GET.get('q')
        
        ClientesHijo = self.request.GET.get('clientesHijo')
        if ClientesHijo:
            queryset = queryset.filter(cliente_hijo=ClientesHijo)

        segregacion = self.request.GET.get('segregacion')
        if segregacion:
            queryset = queryset.filter(tipo_segregacion__nombre=segregacion)

        servicio = self.request.GET.get('servicio')
        if servicio:
            queryset = queryset.filter(servicio__servicio=servicio)

        
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')

        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date() + timedelta(days=1) 
            
        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            queryset = queryset.filter(fecha_creacion__gte=fecha_inicio)
        elif fecha_fin:
            queryset = queryset.filter(fecha_creacion__lte=fecha_fin)

        # Barra de búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(tipo_segregacion__nombre__icontains=search_query) |  
                Q(fecha_creacion__icontains=search_query))  

        id_cliente = self.obtener_id_cliente_padre(self.kwargs['pk'])
        queryset.filter(cliente_padre_id = id_cliente).order_by('-fecha_creacion')

        return queryset

    def get_context_data(self, **kwargs):
        id_cliente = self.obtener_id_cliente_padre(self.kwargs['pk'])

        context = super().get_context_data(**kwargs)
        context['TiposDeServicios'] = TipoDeServicio.objects.all()
        context['TiposDeSegregacion'] = TipoSegregacion.objects.all()
        context['ClientesHijos'] = ClienteHijo.objects.filter(cliente_padre_id=id_cliente)
        return context
  
def cancelar_solicitud_individual(request, pk):
    segregar = SegregarContenedores()

    solicitud = SolicitudIndividual.objects.get(pk=pk)
    if solicitud.estatus_n4 == "Autorizado":
        #Si no hay un error al ejecutar el groovy se elimina el grupo y tipo de operacion
        Error = segregar.eliminar_grupo_tipo_N4(solicitud.contenedor)
        if not Error.get("Error"):
            segregar.eliminar_solicitud(pk)
            
    else:
        segregar.eliminar_solicitud(pk)
    return redirect(request.META.get('HTTP_REFERER', 'core:inicio'))
