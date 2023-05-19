from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.departamento import Departamento
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def gerencia_departamentos(request):
    page_title = "Departamentos"
    count = 0
    departamentos = Departamento.objects.all()
    for p in departamentos:
        count += 1

    return render(request,'departamentos/gerencia_departamentos.html',
    {'departamentos':departamentos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def departamentosTable(request):
    nome = request.GET.get('nome')
    departamentos = Departamento.objects
    if nome:
        departamentos = departamentos.filter(nome__contains = nome)
    departamentos = departamentos.all()
    return render(request,'departamentos/departamentos_table.html',{'departamentos':departamentos})

@login_required(login_url='/auth-user/login-user')
def visualizarDepartamento(request,codigo):
    departamento = Departamento.objects.get(id=codigo)
    return render(request,'departamentos/visualizar_departamento.html',{'departamento':departamento})

@login_required(login_url='/auth-user/login-user')
def departamentosModalCadastrar(request):
    id = request.GET.get('id')
    departamento = None
    data = {}
    if id:
        departamento = Departamento.objects.get(id=id)
        data['departamento'] = departamento
    return render(request,'departamentos/modal_cadastrar_departamento.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarDepartamento(request,codigo):
    departamento = Departamento.objects.get(id=codigo)
    departamento.delete()
    return redirect('/gerenciar-departamentos')

@login_required(login_url='/auth-user/login-user')
def saveDepartamento(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/departamentos', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarDepartamento(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/departamentos/' + str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def departamentosSelect(request):
    data = {}
    if request.GET.get('selected'):
        data['departamento_id'] = int(request.GET.get('selected')) if request.GET.get('selected').strip() else None
    if request.GET.get('departamento_id'):
        data['departamento_id'] = int(request.GET.get('departamento_id')) if request.GET.get('departamento_id').strip() else None
    data["departamentos"] = Departamento.objects.all()

    return render(request,'departamentos/departamentos_select.html', data)