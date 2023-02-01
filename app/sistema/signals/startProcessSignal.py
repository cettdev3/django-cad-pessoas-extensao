from django.core.signals import Signal
from ..services import CamundaAPI
startProcessSignal = Signal()

def startProcessSignalHandler(sender, **kwargs):
    process_id = kwargs.get("process_id")
    response = kwargs.get("response")
    request = kwargs.get("request")
    camundaResponse = CamundaAPI().startProcess(process_id, dados=response.data)
    # print(fsadfsd)
    
startProcessSignal.connect(startProcessSignalHandler)