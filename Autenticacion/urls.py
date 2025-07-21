from django.urls import path

from .views import RegistrarUserPadreView,RegistrarUserAgenteView, RegistrarUserAgenciaView,RegistrarUserHijoView, RegistrarUserHijoView_Admin, cambiar_estado_is_active,EliminarUsuarioView, UsuariosBloqueadosView
from django.contrib.auth import views as auth_views
from . import views

autenticacion_patterns = ([
    # Registro de usuarios
    path('usuarios/crear/padre/', RegistrarUserPadreView.as_view(), name='usuarios_crear_cliente_padre'),
    path('usuarios/crear/hijo/', RegistrarUserHijoView.as_view(), name='usuarios_crear_cliente_hijo'),
    path('usuarios/crear/hijo/admin/<int:pk>/', RegistrarUserHijoView_Admin.as_view(), name='usuarios_crear_cliente_hijo__admin'),
    path('usuarios/crear/agencia/', RegistrarUserAgenciaView.as_view(), name='usuarios_crear_agencia_aduanal'),
    path('usuarios/crear/agente/', RegistrarUserAgenteView.as_view(), name='usuarios_crear_agente_aduanal'),

    # Password reset
    path('usuarios/reset-password/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        html_email_template_name='registration/password_reset_email.html',
    ), name='usuarios_password_reset'),

    # Login / Logout
    path('usuarios/logout/', auth_views.LogoutView.as_view(), name='usuarios_logout'),

    # Administración de usuarios
    path('usuarios/<int:user_id>/bloquear/', views.cambiar_estado_is_active, name='usuarios_bloquear'),
    path('usuarios/<int:pk>/eliminar/', EliminarUsuarioView.as_view(), name='usuarios_eliminar'),
    path('usuarios/bloqueados/', UsuariosBloqueadosView.as_view(), name='usuarios_bloqueados_lista'),
], "autenticacion")
