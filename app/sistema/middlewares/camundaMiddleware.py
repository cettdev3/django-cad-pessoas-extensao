from django.http import HttpResponse
from ..services.gpsProcessService import GPSProcessService
class CamundaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.gpsProcess = GPSProcessService()

    def __call__(self, request):
        route = request.path
        method = request.method
        
        response = self.get_response(request)

        # self.gpsProcess.processar(
        #     route=route, 
        #     method=method, 
        #     response=response
        # )

        return response
