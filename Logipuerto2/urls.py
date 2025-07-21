"""
URL configuration for Logipuerto2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from Clientes.urls import clientes_patterns  
from Core.urls import core_patterns
from Autenticacion.urls import autenticacion_patterns
from Logipuerto2 import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler403
from Core.views import error_403_Personalizado
from Ferrocarril.urls import ferrocarril_patterns
from Solicitudes.urls import solicitudes_patterns
from AgenciamientoAduanal.urls import agenciamiento_aduanal_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(core_patterns)),
    path('autenticacion/', include('django.contrib.auth.urls')),
    path('autenticacion/', include(autenticacion_patterns)),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clientes/', include(clientes_patterns)),
    path('ferrocarril/', include(ferrocarril_patterns)),
    path('Solicitudes/', include(solicitudes_patterns)),
    path('agenciamiento_aduanal/', include(agenciamiento_aduanal_patterns)),
    path('select2/', include('django_select2.urls')),

]

handler403 = error_403_Personalizado
handler404 = error_403_Personalizado

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)