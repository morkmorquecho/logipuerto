import requests
import xmltodict
from xml.etree import ElementTree as ET
from Solicitudes.models import SolicitudIndividual
from Core.mixins import N4GroovyMixin

class ConsultarPreAvisoMixin(N4GroovyMixin):
    """
    Mixin para actualizar solicitudes individuales.
    """
    def Consultar(self, solicitud):
        """
        Actualiza el campo estatusN4 de una solicitud individual si se se retorna un estado 200 de la consulta al web service

        :param solicitudes: Lista de objetos utilizados en la vista (listview) donde fue llamado el metodo
        :return: Consultar en n4 si los contenedores tienen pre-aviso, de ser asi se devuelve true
        """
       
        payload = {"id": solicitud.contenedor}
        print(f"Payload: {payload}")
        url = "http://172.20.79.51:5006/ConsultaLogipuerto"
        # url = "http://cmv41016:8086/ConsultaLogipuerto"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer bb51fb918954a6dc9f9627f3c6300494961dd170fd3b638eda8e3272df8875ef"
        }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Respuesta HTTP {response.status_code}")
            return False, f"Error HTTP {response.status_code}"

        # Verificar la respuesta
        root_dict = xmltodict.parse(response.text)

        try:
            row = root_dict['query-response']['data-table']['rows']['row']
            fields = row['field']
            # <column>Gkey</column>
            # <column>BL</column>
            # <column>Type Arch ISO</column>
            # <column>Buque</column>
            # <column>Contenedor</column>
            # <column>Reefer</column>
            # <column>ETA</column>
            # <column>IMO</column>
            # <column>OOG</column>
            # <column>Viaje</column>
            # <column>Peso Bruto</column>
            # <column>Peso Neto</column>
            # <column>Sello manifestado</column>
            # <column>Sello fisico</column>
            # <column>Sello adicional 1</column>
            # <column>Sello adicional 2</column>
            # <column>Patente</column>

            datos = {
                'Gkey': fields[0],
                'BL': fields[1],
                'Type Arch ISO': fields[2],
                'Buque': fields[3],
                'Contenedor': fields[4],
                'Reefer': fields[5],
                'ETA': fields[6],
                'IMO': fields[7],
                'OOG': fields[8],
                'Viaje': fields[9],
                'Peso Bruto': fields[10],
                'Peso Neto': fields[11],
                'Sello manifestado': fields[12],
                'Sello fisico': fields[13],
                'Sello adicional 1': fields[14],
                'Sello adicional 2': fields[15],
                'Patente': fields[16],  
            }


            return True, datos
        except Exception as e:
            print("Error al interpretar XML:", e)
            return False, "Error al leer XML"

                