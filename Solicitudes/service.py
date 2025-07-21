from django.http import JsonResponse
from Core.mixins import N4GroovyMixin
from Logipuerto2.settings import N4TRAINNING, PASSWORD_N4API, USER_N4API
from Solicitudes.models import SolicitudIndividual
from zeep import Client
import requests
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
import xmltodict
import json
from django.db import connection
from datetime import datetime

def calcular_digito_verificador(contenedor):
    tabla = {
        'A': 10, 'B': 12, 'C': 13, 'D': 14, 'E': 15,
        'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20,
        'K': 21, 'L': 23, 'M': 24, 'N': 25, 'O': 26,
        'P': 27, 'Q': 28, 'R': 29, 'S': 30, 'T': 31,
        'U': 32, 'V': 34, 'W': 35, 'X': 36, 'Y': 37,
        'Z': 38
    }
    pesos = [2**i for i in range(10)]
    valores = []

    for i, c in enumerate(contenedor[:10]):
        val = int(c) if c.isdigit() else tabla.get(c.upper(), 0)
        valores.append(val * pesos[i])

    total = sum(valores)
    digito = total % 11
    return 0 if digito == 10 else digito

def verificar_contenedor(request, numero):
    if len(numero) != 11:
        return numero, False


    calculado = calcular_digito_verificador(numero)
    valido = int(numero[-1]) == calculado

    return numero, valido
# MEDU3215089