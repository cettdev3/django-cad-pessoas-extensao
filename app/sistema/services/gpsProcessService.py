import envconfiguration as env_config
from requests.auth import HTTPBasicAuth
from django.http import HttpRequest
from rest_framework.request import Request
from rest_framework.decorators import api_view
from ..signals.completeTaskSignal import completeTaskSignal
from ..signals.startProcessSignal import startProcessSignal
import json
from rest_framework.parsers import FormParser

from ..models import Ensino

class GPSProcessService:
    def __init__(self):
        self.process_id = "Process_0ujigdr"

    def processar(self, **kwargs):
        route = kwargs.get("route")
        method = kwargs.get("method")
        response = kwargs.get("response")

        if response.status_code != 200 and response.status_code != 201:
            return
        # print("rota", route, "metodo", method, "request", request, "response", response)
        if route == "/ensino" and method == "POST":
            self.iniciarProcesso(response)
        elif route == "/alocacoes" and method == "POST":
            self.solicitarCursos(response)

    def iniciarProcesso(self, response):
        tipo = json.loads(response.content).get("tipo")
        if tipo == 'gps':
            startProcessSignal.send(
                sender=self.__class__,
                process_id=self.process_id,
                response=response,
                variables={}
            )

    def solicitarCursos(self, response):
        taskID = "SolicitarCursosTask"
        response = json.loads(response.content)
        isList = type(response) == list
        acaoEnsinoId = response[0].get("acaoEnsino")["id"] if isList else response.get("acaoEnsino")["id"]
        acaoEnsino = Ensino.objects.prefetch_related("alocacao_set").get(id=acaoEnsinoId)
        alocacaoesCadastradas = len(acaoEnsino.alocacao_set.all())
        alocacaoesSolicitadas = len(response) if isList else 1
        if alocacaoesCadastradas == alocacaoesSolicitadas:
            completeTaskSignal.send(
                sender=self.__class__,
                process_id=self.process_id,
                task_id=taskID,
                variables={}
            )