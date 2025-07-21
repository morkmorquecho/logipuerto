
from django.urls import path
from .views import FerrocarrilView, SegregacionView, SolicitudesIndividualesFerroView, FerrocarrilTransporteView, EscogerContenedoresView, CrearSolicitudesIndividualesTransporteView

ferrocarril_patterns = ([
    #Segregacion
    path('inicio/', FerrocarrilView.as_view(), name="ferrocarril_inicio"),
    path('segregaciones/', SegregacionView.as_view(), name="ferrocarril_segregaciones"),
    path('solicitudes-individuales/<int:pk>/', SolicitudesIndividualesFerroView.as_view(), name="ferrocarril_solicitud_individual_ver"),

    #Ferro Transporte
    path('transporte/', FerrocarrilTransporteView.as_view(), name="ferrocarril_ferro_transporte"),
    path('transporte/contenedores/', EscogerContenedoresView.as_view(), name="ferrocarril_transporte_escoger_contenedor" ),
    path('transporte/solicitudes-masivas/crear', CrearSolicitudesIndividualesTransporteView.as_view(), name = "ferrocarril_transporte_crear_solicitud_masiva")
], "ferrocarril")

