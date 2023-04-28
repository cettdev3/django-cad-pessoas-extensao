from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.serializers.escolaSerializer import EscolaSerializer
from sistema.models.curso import Curso
from sistema.models.endereco import Endereco
from sistema.models.escola import Escola
from sistema.models.cidade import Cidade
from sistema.models.ensino import Ensino
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def gerencia_ensinos(request):
    page_title = "Ações de Ensino"
    count = 0
    ensinos = Ensino.objects.all()
    for p in ensinos:
        count += 1

    return render(request,'ensinos/gerencia_ensinos.html',
    {'ensinos':ensinos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def ensinosTable(request):
    token, created = Token.objects.get_or_create(user=request.user)
    
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/ensino', params={
        'order_by': request.GET.get('order_by'),
        'observacao': request.GET.get('observacao'),
        'data_inicio': request.GET.get('data_inicio'),
        'data_fim': request.GET.get('data_fim'),
        'escolas': request.GET.getlist('escolas[]'),
    }, headers=headers)
    ensinos = json.loads(response.content)
    return render(request,'ensinos/ensinos_table.html',{'ensinos':ensinos})

@login_required(login_url='/auth-user/login-user')
def visualizarEnsino(request,codigo):
    ensino = Ensino.objects.get(id=codigo)
    page_title = ensino.observacao
    path_back = "gerenciar-ensinos"
    return render(request,'ensinos/visualizar_ensino.html',{
        'ensino':ensino, 
        'page_title': page_title,
        'path_back': path_back
    })

@login_required(login_url='/auth-user/login-user')
def ensinosModalCadastrar(request):
    id = request.GET.get('id')
    ensino = None
    escolas = Escola.objects.all()
    data = {}
    if id:
        ensino = Ensino.objects.get(id=id)
        data['ensino'] = EnsinoSerializer(ensino).data
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    return render(request,'ensinos/modal_cadastrar_ensino.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarEnsino(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.delete('http://localhost:8000/ensino/'+str(codigo), headers=headers)
    print(response.content)
    if response.status_code == 204:
        messages.success(request, 'Ensino eliminado com sucesso!')
    else:
        messages.error(request, 'Erro ao eliminar evento!')
    return redirect('/gerenciar-ensinos', messages)

@login_required(login_url='/auth-user/login-user')
def saveEnsino(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print(body)
    response = requests.post('http://localhost:8000/ensino', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarEnsino(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/ensino/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def getEnsino(request, ensino_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/ensino/'+str(ensino_id), headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)