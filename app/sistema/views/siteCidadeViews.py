from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.cidade import Cidade
from sistema.models.curso import Curso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_cidades(request):
    page_title = "Cidades"
    count = 0
    cidades = Cidade.objects.all()
    for p in cidades:
        count += 1

    return render(request,'cidades/gerencia_cidades.html',
    {'cidades':cidades,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def cidadesTable(request):
    nome = request.GET.get('nome')
    cidades = Cidade.objects
    if nome:
        cidades = cidades.filter(nome__contains = nome)
    cidades = cidades.all()
    return render(request,'cidades/cidades_table.html',{'cidades':cidades})

@login_required(login_url='/auth-user/login-user')
def visualizarCidade(request,codigo):
    cidade = Cidade.objects.get(id=codigo)
    return render(request,'cidades/visualizar_cidade.html',{'cidade':cidade})

@login_required(login_url='/auth-user/login-user')
def cidadesModalCadastrar(request):
    id = request.GET.get('id')
    cidade = None
    data = {}
    if id:
        cidade = Cidade.objects.get(id=id)
        data['cidade'] = cidade
    return render(request,'cidades/modal_cadastrar_cidade.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarCidade(request,codigo):
    cidade = Cidade.objects.get(id=codigo)
    cidade.delete()
    return redirect('/gerenciar-cidades')

@login_required(login_url='/auth-user/login-user')
def saveCidade(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/cidades', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarCidade(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/cidades/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def cidadesSelect(request):
    data = {}
    if request.GET.get('selected'):
        data['cidade_id'] = int(request.GET.get('selected')) if request.GET.get('selected').strip() else None
    if request.GET.get('cidade_id'):
        data['cidade_id'] = int(request.GET.get('cidade_id')) if request.GET.get('cidade_id').strip() else None
    data["cidades"] = Cidade.objects.all()

    return render(request,'cidades/cidades_select.html', data)