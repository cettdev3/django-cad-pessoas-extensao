import envconfiguration as env_config
from requests.auth import HTTPBasicAuth
from ..signals.completeTaskSignal import completeTaskSignal
from ..signals.startProcessSignal import startProcessSignal

class GPSProcessService:
    def __init__(self):
        self.process_name = "gps"

    def processGps(self, **kwargs):
        route = kwargs.get("route")
        method = kwargs.get("method")
        request = kwargs.get("request")
        response = kwargs.get("response")

        if route == "/ensino" and method == "POST":
            self.iniciarProcesso(request, response)

        return "json_object"

    def iniciarProcesso(self, request, response):
        startProcessSignal.send(
            sender=self.__class__,
            process_id=self.process_name,
            response=response,
            request=request,
            variables={}
        )
        
        return "json_object"
   
    def solicitarCursos(self):
        completeTaskSignal.send(
            sender=self.__class__, 
            process_id=self.process_name, 
            task_id="iniciarProcesso", 
            variables={}
        )
        
        return "json_object"