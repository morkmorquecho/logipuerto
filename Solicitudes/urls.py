from django.urls import path
from .views import CrearTipoSegregacionView, ListaSolicitudesMasivasAdminView, ListaSolicitudesMasivasUserPadreView, cancelar_solicitud_individual


solicitudes_patterns = ([

    #Tipo de segregación
    path('tipos-de-segregacion/crear/', CrearTipoSegregacionView.as_view(), name="solicitudes_tipo_segregacion_crear" ),

    #solicitudes masivas
    path('solicitudes-masivas/admin/', ListaSolicitudesMasivasAdminView.as_view(), name="solicitudes_masivas__admin" ),
    path('solicitudes-masivas/cliente-padre/<int:pk>/', ListaSolicitudesMasivasUserPadreView.as_view(), name="solicitudes_masivas__cliente_padre"),

    #solicitud individual
    path('solicitudes-individuales/<int:pk>/cancelar/', cancelar_solicitud_individual, name="solicitudes_individual_cancelar"),

], "solicitudes")



