from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.http import JsonResponse
from django.db import connection, reset_queries
from django.core import serializers
import requests
import json
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import render, redirect
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.serializers.pessoaSerializer import PessoaSerializer
from sistema.serializers.userSerializer import UserSerializer
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.serializers.turnoSerializer import TurnoSerializer
from sistema.models.pessoa import Pessoas
from rest_framework.authtoken.models import Token
from sistema.models.curso import Curso
from sistema.models.ensino import Ensino
from sistema.models.turno import Turno
from django.db.models import Q, Exists
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_pessoas(request):
    page_title = "Pessoas"
    count = 0

    return render(request,'pessoas/gerencia_pessoas.html',
    {'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def pessoasTable(request):
    token, created = Token.objects.get_or_create(user=request.user)

    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/pessoas', params={
        'nome': request.GET.get('nome'),
        'data_inicio': request.GET.get('data_inicio'),
        'data_fim': request.GET.get('data_fim'),
        'is_alocated': request.GET.get('is_alocated'),
    }, headers=headers)
    pessoas = json.loads(response.content)
    return render(request,'pessoas/pessoas_table.html',{'pessoas':pessoas})

@login_required(login_url='/auth-user/login-user')
def visualizarPessoa(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/pessoas/'+codigo, headers=headers)
    pessoa = json.loads(response.content)
    return render(request,'pessoas/visualizar_pessoas.html',{'pessoa':pessoa})

@login_required(login_url='/auth-user/login-user')
def pessoasModalCadastrar(request):
    print("request",request)
    id = request.GET.get('id')
    pessoa = None
    cursos = None
    users = User.objects.all()

    if id:
        token, created = Token.objects.get_or_create(user=request.user)
    
        headers = {'Authorization': 'Token ' + token.key}
        response = requests.get('http://localhost:8000/pessoas/'+id, headers=headers)
        pessoa = json.loads(response.content)
        if pessoa["cursos"]:
            pessoa = pessoa
            cursos = pessoa["cursos"]
        print(pessoa)
    print("usuarios", UserSerializer(users, many=True).data)
    return render(request,'pessoas/modal_cadastrar_pessoa.html',{'pessoa':pessoa, 'cursos':cursos, 'users':users})

@login_required(login_url='/auth-user/login-user')
def pessoasModalAlocar(request):
    pessoaIds = request.GET.getlist('checked_values[]')
    turnos = Turno.objects.all()
    turnos = TurnoSerializer(turnos, many=True)
    data = {}
    data["turnos"]  = turnos.data
    if pessoaIds:
        pessoas = Pessoas.objects.filter(id__in=pessoaIds).all()
        pessoas = PessoaSerializer(pessoas, many = True)
        data['pessoas'] = pessoas.data
        ensinos = Ensino.objects.filter(~Q(status="finalizado"))
        ensinos = EnsinoSerializer(ensinos, many=True)
        data['ensinos'] = ensinos.data

    return render(request,'pessoas/modal_alocar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def cursosSelect(request):
    cursos = Curso.objects.all()
    return render(request,'pessoas/cursos_select.html',{'cursos':cursos})

@login_required(login_url='/auth-user/login-user')
def pessoasSelect(request):
    pessoas = Pessoas.objects.all()
    return render(request,'pessoas/pessoas_select.html',{'pessoas':pessoas})

@login_required(login_url='/auth-user/login-user')
def eliminarPessoa(request,codigo):
    user = Pessoas.objects.get(id=codigo)
    user.delete()
    return redirect('/gerenciar-pessoas')


@login_required(login_url='/auth-user/login-user')
def savePessoa(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/pessoas', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)


@login_required(login_url='/auth-user/login-user')
def editarPessoa(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/pessoas/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

# FIM PESSOAS