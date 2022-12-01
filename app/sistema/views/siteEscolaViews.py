from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.escolaSerializer import EscolaSerializer
from sistema.models.escola import Escola
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_escolas(request):
    page_title = "Escolas"
    count = 0
    escolas = Escola.objects.all()
    for p in escolas:
        count += 1

    return render(request,'escolas/gerencia_escolas.html',
    {'escolas':escolas,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def escolasTable(request):
    nome = request.GET.get('nome')
    escolas = Escola.objects
    if nome:
        escolas = escolas.filter(nome__contains = nome)
    escolas = escolas.all()
    return render(request,'escolas/escolas_table.html',{'escolas':escolas})

@login_required(login_url='/auth-user/login-user')
def visualizarEscola(request,codigo):
    escola = Escola.objects.get(id=codigo)
    return render(request,'escolas/visualizar_escola.html',{'escola':escola})

@login_required(login_url='/auth-user/login-user')
def escolasModalCadastrar(request):
    id = request.GET.get('id')
    escola = None
    data = {}
    if id:
        escola = Escola.objects.get(id=id)
        data['escola'] = EscolaSerializer(escola).data
    return render(request,'escolas/modal_cadastrar_escola.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarEscola(request,codigo):
    escola = Escola.objects.get(id=codigo)
    escola.delete()
    return redirect('/gerenciar-escolas')

@login_required(login_url='/auth-user/login-user')
def saveEscola(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/escolas', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarEscola(request, escola_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/escolas/'+str(escola_id), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def escolasSelect(request):
    escolas = Escola.objects.all()
    return render(request,'escolas/escolas_select.html',{'escolas':escolas})
