from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.pessoa import Pessoas
from sistema.models.cidade import Cidade
from sistema.models.acao import Acao
from django.contrib.auth.decorators import login_required
import requests
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from django.http import JsonResponse

@login_required(login_url='/auth-user/login-user')
def saveItinerarioItem(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/itinerario-itens', json=body, headers=headers)
    return JsonResponse(json.loads(response.content.decode()),status=response.status_code, safe=False)

@login_required(login_url='/auth-user/login-user')
def editarItinerarioItem(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/itinerario-itens/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarItinerarioItem(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/itinerario-itens/'+str(codigo), headers=headers)
    
    return HttpResponse(status=response.status_code)