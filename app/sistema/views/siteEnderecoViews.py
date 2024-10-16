from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.models.curso import Curso
from sistema.models.endereco import Endereco
from sistema.models.cidade import Cidade
from sistema.models.ensino import Ensino 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def saveEndereco(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/enderecos', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarEndereco(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/enderecos/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def enderecosSelect(request):
    enderecos = Endereco.objects
    if request.GET.get('cidade_id'):
        cidade_id = request.GET.get('cidade_id')
        enderecos = enderecos.filter(cidade_id=cidade_id)

    enderecos = enderecos.all()
    return render(request,'enderecos/enderecos_select.html',{'enderecos':enderecos})