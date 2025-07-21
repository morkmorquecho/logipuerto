from datetime import datetime
from zeep import Client
import requests
from django.http import HttpResponse
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
import os
from requests.auth import HTTPBasicAuth
import xmltodict
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
import sentry_sdk
import logging
from Logipuerto2.settings import N4TRAINNING, PASSWORD_N4API, USER_N4API
import openpyxl

#esta clase mixin permite manejar los messages de django, util para no repetirar el mismo codigo en cada vista adaptado igual para ser utilizado en sweetAlerts
class MessageMixin:
    def add_message(self, level, message, extra_tags='', fail_silently=False):
        messages.add_message(
            self.request,
            level,
            message,
            extra_tags=extra_tags,
            fail_silently=fail_silently
        )

    def success(self, message, **kwargs):
        self.add_message(messages.SUCCESS, message, **kwargs)

    def error(self, message, **kwargs):
        self.add_message(messages.ERROR, message, **kwargs)

    def info(self, message, **kwargs):
        self.add_message(messages.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self.add_message(messages.WARNING, message, **kwargs)

#este mixin es utilizado para el restablecimiento de contraseña, enviando un correo al usuario con un link para restablecer la contraseña
class PasswordResetEmailMixin:
    password_reset_template = 'registration/password_reset_email.html'
    site_name = 'Logipuerto'

    def enviar_password_reset_email(self, correo, username, welcome):
        form = PasswordResetForm({'email': correo})
        if not form.is_valid():
            raise ValidationError(f"Email inválido: {form.errors.as_text()}")

        form.save(
            use_https=self.request.is_secure(),
            request=self.request,
            email_template_name=self.password_reset_template,
            html_email_template_name=self.password_reset_template,
            extra_email_context={
                'welcome': welcome,
                'site_name': self.site_name,
                'username': username
            }
        )

#Este mixin es utilizado para verificar si el usuario tiene permisos para acceder a una vista, si no tiene permisos lanza un error 403
class GroupRequiredMixin(AccessMixin):
    group_required = None #Logipuerto, Administrador, ClientePadre, ClienteHijo

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        group_required = self.group_required
        if isinstance(group_required, str):
            group_required = [group_required]

        if request.user.groups.filter(name__in=group_required).exists() or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied  # lanza 403
    
#Forma senculla de ejecutar groovys de n4, solo se necesita proporcionar el nombre del groovy, los parametros y datos (IMPORTANTE LOS PARAMETROS Y DATOS TIENE QUE MANDARSE COMO LISTA [1,2,3,4] ASI SEA UNO SOLO)
class N4GroovyMixin():
    UrlN4 = N4TRAINNING
    UserN4 = USER_N4API
    PasswordN4 = PASSWORD_N4API

    def __init__(self) -> None:
        super().__init__()
        self.Cliente = self.Conexion()

    def Conexion(self):
        wsdl = self.UrlN4 + "services/argobasicservice?wsdl"
        session = Session()
        session.auth = HTTPBasicAuth(self.UserN4, self.PasswordN4)
        client = Client(wsdl, transport=Transport(session=session))
        return client
        

    def EjecutarGroovy(self, IdParametros, Parametros, NombreGroovy):
        try:
            parametros_xml = ""
            
            for id_param, val_param in zip(IdParametros, Parametros):
                parametros_xml += f'<parameter id="{id_param}" value="{val_param}"/>\n'

            RequestData = f'''
                <groovy class-name="{NombreGroovy}" class-location="database">
                    <parameters>
                        {parametros_xml.strip()}
                    </parameters>
                </groovy>
            '''

            Respuesta = self.Cliente.service.basicInvoke(
                scopeCoordinateIds="ICT/CMSA/ZLO/TEC2", xmlDoc=RequestData
            )

            # Validar si hay respuesta
            if not Respuesta:
                sentry_sdk.capture_message(f"Groovy '{NombreGroovy}' sin respuesta", level="error")
                return {"Error": True, "MsjError": "No se recibió respuesta del servicio."}

            ResultadoN4 = xmltodict.parse(Respuesta)
            estatus = ResultadoN4.get("argo-response", {}) \
                                .get("respuestaN4", {}) \
                                .get("@estatus")

            # Validar estructura de la respuesta
            RespuestaN4 = (
                ResultadoN4
                .get("argo-response", {})
                .get("respuestaN4", {})
            )

            # Validar si hay un error en la respuesta
            if RespuestaN4.get("@estatus") == "ERROR":
                sentry_sdk.capture_message(f"Error en ejecución de '{NombreGroovy}': {RespuestaN4.get('errores')}", level="error")
                return {
                    "Error": True,
                    "MsjError": RespuestaN4.get("errores", {}).get("error", "Error desconocido."),
                }
            print("este es el statuuuuuuuuuuuuuuuus")
            print(estatus)
            if estatus == "OK":
                return {
                    "Error": False,
                    "MsjError": "El servicio respondió  estatus OK"
                }
            else: 
                with sentry_sdk.push_scope() as scope:
                    scope.set_tag("Aplicacion", "Logipuerto")
                    scope.set_tag("groovy", NombreGroovy)
                    scope.set_context("parametros", dict(zip(IdParametros, Parametros)))
                    scope.set_context("respuesta_xml", ResultadoN4)
                    sentry_sdk.capture_message(
                        f"Error en ejecución de '{NombreGroovy}'", level="error"
                    )
                return {
                    "Error": True,
                    "MsjError": "El servicio no responde. Requiere verificación manual."
                }
                    
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("groovy", NombreGroovy)
                scope.set_context("parametros", dict(zip(IdParametros, Parametros)))
                sentry_sdk.capture_exception(e)
            return {"Error": True, "MsjError": "Excepción en la ejecución del groovy"}
        
#Manejador de errores con Sentry implementado, engloba toda la clase Exception
logger = logging.getLogger(__name__)
class ErrorHandlingMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            self.reportar_error(e, request)
            from django.shortcuts import redirect
            return redirect('core:error')  

    def reportar_error(self, exception, request):
        with sentry_sdk.push_scope() as scope:
            if request.user.is_authenticated:
                scope.set_user({
                    "id": request.user.id,
                    "username": request.user.username
                })
            scope.set_tag("Aplicacion", "Logipuerto")
            scope.set_tag("path", request.path)
            scope.set_tag("method", request.method)
            scope.set_extra("kwargs", self.kwargs)
            logger.error("Error capturado", exc_info=exception)

            sentry_sdk.capture_exception(exception)

class ControladorExcelMixin:
    import openpyxl  # Asegúrate de tener este import
    from django.http import HttpResponse
    from django.db.models import Q
    @staticmethod
    def convertir_queryset_a_excel(queryset, headers, row_func, filename="archivo.xlsx", sheet_title="Datos"):
        """
        Exporta un queryset a Excel.
        
        - headers: lista de strings (encabezados de columnas)
        - row_func: función que recibe un objeto y devuelve una lista de valores
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = sheet_title

        ws.append(headers)

        for obj in queryset:
            ws.append(row_func(obj))

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"

        wb.save(response)
        return response
