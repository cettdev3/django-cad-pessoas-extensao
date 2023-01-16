from django.contrib.auth.decorators import login_required
import requests
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from django.http import JsonResponse

@login_required(login_url='/auth-user/login-user')
def saveItinerario(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print("body dentro do front: ",body)
    response = requests.post('http://localhost:8000/itinerarios', json=body, headers=headers)
    return JsonResponse(json.loads(response.content.decode()),status=response.status_code, safe=False)

@login_required(login_url='/auth-user/login-user')
def editarItinerario(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print("dentro da view do site",body)
    response = requests.put('http://localhost:8000/itinerarios/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarItinerario(request,codigo):
    print("item de itinerario a ser deletado: ", codigo)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/itinerarios/'+str(codigo), headers=headers)
    print(response.content)
    return HttpResponse(status=response.status_code)