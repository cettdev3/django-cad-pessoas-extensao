from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.servicoContratadoSerializer import ServicoContratadoSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def servicoContratadoModal(request):
    servico_contratado_id = request.GET.get('servico_contratado_id')
    dp_evento_id = request.GET.get('dp_evento_id')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/servicos-contratados/' + str(servico_contratado_id) if servico_contratado_id else 'http://localhost:8000/servicos-contratados'
    response = requests.get(
        url, 
        headers=headers
    )

    servicoContratado = json.loads(response.content)
    return render(
        request,
        'servicosContratados/modal_servico_contratado.html',
        {'servicoContratado':servicoContratado, 'dp_evento_id':dp_evento_id}
    )

@login_required(login_url='/auth-user/login-user')
def servicoContratadoTable(request):
    dp_evento_id = request.GET.get('dp_evento_id')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get(
        'http://localhost:8000/servicos-contratados', 
        params={
            'dp_evento_id': dp_evento_id
        }, 
        headers=headers
    )

    servicosContratados = json.loads(response.content)
    return render(
        request,
        'servicosContratados/servicos_contratados_table.html',
        {'servicosContratados':servicosContratados, 'dp_evento_id':dp_evento_id}
    )

@login_required(login_url='/auth-user/login-user')
def saveServicoContratado(request):
    payload = json.loads(request.body)
    servico_contratado_id = payload.pop('servico_contratado_id', None)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/servicos-contratados/' + str(servico_contratado_id) if servico_contratado_id else 'http://localhost:8000/servicos-contratados'
    body = payload
    response = None
    if servico_contratado_id:
        response = requests.put(url,json=body,headers=headers)
    else:
        response = requests.post(url,json=body,headers=headers)
    print(fasfs)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})

@login_required(login_url='/auth-user/login-user')
def deleteServicoContratado(request, servico_contratado_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/servicos-contratados/' + str(servico_contratado_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})