from django.core.signals import Signal
from ..services import CamundaAPI
from ..models import Ensino
import json

startProcessSignal = Signal()

def startProcessSignalHandler(sender, **kwargs):
    process_id = kwargs.get("process_id")
    response = kwargs.get("response")
    request = kwargs.get("request")

    response = json.loads(response.content)
    camundaApi = CamundaAPI()
    
    camundaVariables = {"variables": {}}
    for key, value in response.items():
        camundaVariables["variables"].update(camundaApi.camundaVariableFormat(key, value, "String"))
    camundaResponse = camundaApi.startProcess(process_id, dados=camundaVariables)
    process_instance_id = camundaResponse["id"]
    acaoEnsino = Ensino.objects.get(id=response["id"])
    acaoEnsino.process_instance = process_instance_id
    acaoEnsino.save()
    
startProcessSignal.connect(startProcessSignalHandler)