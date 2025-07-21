from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Core.mixins import MessageMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseForbidden

from Clientes.models import ClientePadre

# Create your views here.
class HomePageView(LoginRequiredMixin, MessageMixin, TemplateView):
    template_name = "Core/inicio.html"
    login_url = '/autenticacion/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario_actual = self.request.user
        grupos = usuario_actual.groups.all()
        print(usuario_actual)
        for grupo in grupos:
            print(grupo.name)
        return context
    
class ErrorPage(TemplateView):
    template_name = "Core/500.html"

#vista error 404 personalizada
# @csrf_exempt  
# def custom_404(request, exception=None):
#     try:
#         return render(request, 'Core/404.html', {}, status=404)
#     except TemplateDoesNotExist:
#         # Respuesta de emergencia si la plantilla no existe
#         return HttpResponseNotFound(
#             '<h1>404 Página no encontrada</h1><p>La página solicitada no existe.</p>',
#             content_type='text/html'
#         )


def error_403_Personalizado(request, exception=None):
    return render(request, 'Core/403.html', status=403)

