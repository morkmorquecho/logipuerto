from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView, DetailView, UpdateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.contrib.auth.models import User
from .form import Pagina1Form, Pagina2Form, Pagina3Form, Pagina4Form, Pagina5Form 
from Core.constants import ESTADOS_MEXICO
from Core.mixins import ControladorExcelMixin, GroupRequiredMixin
from django.template.loader import get_template
from Core.mixins import MessageMixin
from .models import ClienteHijo, ClientePadre,ContactoClientePadre, Documentos

# Create your views here.
class ListaClientesPadreView(GroupRequiredMixin, MessageMixin,ListView):
    Paginacion = 2
    model = ClientePadre
    context_object_name = 'listadoClientesPadres'
    paginate_by = Paginacion 
    ordering = ['-fecha_creacion']
    group_required = ["Logipuerto", "Administrador"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        # Filtro por país
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(pais=country)  
            
        # Filtro por estado
        estado = self.request.GET.get('estado') 
        if estado:  
            queryset = queryset.filter(estado=estado)

        #Barra de búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(rfc__icontains=search_query) | 
                Q(razon_social__icontains=search_query)
            )
        return queryset
        
    def get_context_data(self, **kwargs):
        hoy = date.today() 
        hace_7_dias = hoy - timedelta(days=7)

        context = super().get_context_data(**kwargs)
        context['TotalUsuarios'] =  User.objects.count() 
        context['Bloqueados'] = User.objects.filter(is_active = False).count()
        context['Activos'] = User.objects.filter(is_active = True).count()
        context['Nuevos'] = User.objects.filter(date_joined__gte =  hace_7_dias).count
        context['estados'] = ESTADOS_MEXICO  # Agrega el diccionario al contexto

        return context

    # def exportar_clientes_padres_excel(self, request):
    #     qs = self.get_queryset()
    #     headers = ['ID', 'RFC', 'Razon Social', 'Tipo RFC', 'Pais', 'Estado', 'Status']
        
    #     def fila(obj):
    #         return [
    #             obj.id,
    #             obj.rfc,
    #             obj.razon_social,
    #             obj.tipo_rfc,
    #             obj.pais,
    #             obj.estado,
    #             obj.user.is_active
    #         ]

    #     return self.convertir_queryset_a_excel(
    #         queryset=qs,
    #         headers=headers,
    #         row_func=fila,
    #         filename="ClientesPadre.xlsx",
    #         sheet_title="Lista de Clientes Padres"
    #     )

class DetalleClientePadreView(GroupRequiredMixin, DetailView):
    model = ClientePadre
    context_object_name = 'clientePadre'
    group_required = ["Logipuerto", "Administrador"]
    template_name = "Clientes/ClientePadre_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related(
            'contactoclientepadre',
            'documentos'
        ).prefetch_related(
            Prefetch('hijos', 
                    queryset=ClienteHijo.objects.select_related('user'))
        )
    

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['clientes_hijos'] = self.object.hijos.all()
        context['cantidad_hijos'] = self.object.hijos.count()
        context['contacto'] = self.object.contactoclientepadre
        context['documentos'] = self.object.documentos
        context['hijos'] = self.object.hijos.all()
        return context

class ListaClientesHijoView(GroupRequiredMixin, ListView):
    model = ClienteHijo
    context_object_name = 'listadoClientesHijos'
    paginate_by = 20  
    ordering = ['-fecha_creacion']
    group_required = ["Administrador", "ClientePadre", "Logipuerto"]

    def get_queryset(self):
        cliente_padre = get_object_or_404(ClientePadre, user=self.kwargs['pk'])
        return ClienteHijo.objects.filter(cliente_padre_id = cliente_padre)


def editar_cliente(request, pk):
    cliente_padre = get_object_or_404(ClientePadre, pk=pk)
    
    # Obtener o crear instancias relacionadas
    contacto, _ = ContactoClientePadre.objects.get_or_create(cliente_padre=cliente_padre)
    documentos, _ = Documentos.objects.get_or_create(cliente_padre=cliente_padre)
    
    if request.method == 'POST':
        form1 = Pagina1Form(request.POST, instance=cliente_padre)
        form2 = Pagina2Form(request.POST, instance=cliente_padre)
        form3 = Pagina3Form(request.POST, instance=cliente_padre)
        contacto_form = Pagina4Form(request.POST, instance=contacto)
        documentos_form = Pagina5Form(request.POST, request.FILES, instance=documentos)
        
        if all([form1.is_valid(), form2.is_valid(), form3.is_valid(), 
                contacto_form.is_valid(), documentos_form.is_valid()]):
            form1.save()
            form2.save()
            form3.save()
            contacto_form.save()
            documentos_form.save()
            return redirect('clientes:clientes_padre_detalle', pk=pk)
        else:         
            print("Form1:", form1.errors)
            print("Form2:", form2.errors)
            print("Form3:", form3.errors)  
            print("contacto_form:", contacto_form.errors)
            print("documentos_form", documentos_form.errors)
  
                    
    else:
        form1 = Pagina1Form(instance=cliente_padre)
        form2 = Pagina2Form(instance=cliente_padre)
        form3 = Pagina3Form(instance=cliente_padre)
        contacto_form = Pagina4Form(instance=contacto)
        documentos_form = Pagina5Form(instance=documentos)
    
    contacto = ContactoClientePadre.objects.filter(cliente_padre=cliente_padre).first()
    documentos = Documentos.objects.filter(cliente_padre=cliente_padre).first()
    user = cliente_padre.user    
    
    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'contacto_form': contacto_form,
        'documentos_form': documentos_form,
        'cliente': cliente_padre,
        'contacto': contacto,
        'documentos': documentos,
        'user' : user,
    }

    
    return render(request, 'Clientes/ClientePadre_update.html', context)
        

# Manejo de VDV (Validar Digito Verificador)
def manejo_vdv(request, pk):
    
    #Validador de Digito Verificador
    VDV = get_object_or_404(ClientePadre, pk=pk)
    nuevo_estado = not VDV.digito_verificador 
    VDV.digito_verificador = nuevo_estado
    VDV.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'core:inicio'))


def exportar_clientes_padres_excel(request):
    queryset = ClientePadre.objects.all().order_by('-fecha_creacion')

    # Reconstrucción manual de filtros como en la clase original
    search_query = request.GET.get('q')
    country = request.GET.get('country')
    estado = request.GET.get('estado')

    if country:
        queryset = queryset.filter(pais=country)
    if estado:
        queryset = queryset.filter(estado=estado)
    if search_query:
        queryset = queryset.filter(
            Q(rfc__icontains=search_query) | 
            Q(razon_social__icontains=search_query)
        )

    # Define los headers y la función para las filas
    headers = ['ID', 'RFC', 'Razon Social', 'Tipo RFC', 'Pais', 'Estado', 'Status']
    def fila(obj):
        return [
            obj.id,
            obj.rfc,
            obj.razon_social,
            obj.tipo_rfc,
            str(obj.pais.name),
            obj.estado,
            'Activo' if obj.user.is_active else 'Bloqueado'
        ]

    # Llamada al helper para generar el Excel (puede venir de un Mixin o util)
    return ControladorExcelMixin.convertir_queryset_a_excel(        
        queryset=queryset,
        headers=headers,
        row_func=fila,
        filename="ClientesPadre.xlsx",
        sheet_title="Lista de Clientes Padres"
    )

#Lista de clientes padres con validador de digito verificador desactivado
class ListaClientePadreVDV_View(GroupRequiredMixin, ListView):
    model = ClientePadre
    context_object_name = 'listadoClientesPadresVDV'
    paginate_by = 20  
    ordering = ['-fecha_creacion']
    template_name = 'Clientes/ClientePadreVDV_list.html'
    group_required = ["Logipuerto", "Administrador"]

    def get_queryset(self):
        return ClientePadre.objects.filter(digito_verificador=False)
