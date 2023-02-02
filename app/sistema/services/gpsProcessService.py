import envconfiguration as env_config
from requests.auth import HTTPBasicAuth
from ..signals.completeTaskSignal import completeTaskSignal
from ..signals.startProcessSignal import startProcessSignal
import json

class GPSProcessService:
    def __init__(self):
        self.process_id = "Process_0ujigdr"

    def processar(self, **kwargs):
        route = kwargs.get("route")
        method = kwargs.get("method")
        request = kwargs.get("request")
        response = kwargs.get("response")


        if response.status_code != 200 and response.status_code != 201:
            return

        if route == "/ensino" and method == "POST":
            self.iniciarProcesso(request, response)

    def iniciarProcesso(self, request, response):
        tipo = json.loads(response.content).get("tipo")
        if tipo == 'gps':
            startProcessSignal.send(
                sender=self.__class__,
                process_id=self.process_id,
                response=response,
                request=request,
                variables={}
            )
   
    def solicitarCursos(self):
        completeTaskSignal.send(
            sender=self.__class__, 
            process_id=self.process_id, 
            task_id="iniciarProcesso", 
            variables={}
        )