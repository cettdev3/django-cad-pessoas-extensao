from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.http import JsonResponse
from django.db import connection, reset_queries
from django.core import serializers
from django.db.models import Count
from django.shortcuts import render, redirect
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.serializers.pessoaSerializer import PessoaSerializer
from sistema.serializers.eventoSerializer import EventoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.curso import Curso
from sistema.models.evento import Evento
from django.db.models import Q, Exists
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_pessoas(request):
    page_title = "Pessoas"
    count = 0
    pessoa = Pessoas.objects.all()
    for p in pessoa:
        count += 1

    return render(request,'pessoas/gerencia_pessoas.html',
    {'pessoas':pessoa,'contagem':count, "page_title": page_title})

# @login_required(login_url='/auth-user/login-user')
def pessoasTable(request):
    nome = request.GET.get('nome')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    pessoas = Pessoas.objects
    if nome:
        pessoas = pessoas.filter(nome__contains = nome)
    if data_fim and data_inicio:
        pessoas = pessoas.filter(
            ~Exists(Pessoas.objects.filter(
                Q(alocacao__data_inicio__gte=data_inicio,
                alocacao__data_inicio__lte=data_fim) |
                Q(alocacao__data_fim__gte=data_inicio,
                alocacao__data_fim__lte=data_fim) 
            ))
        ).union(pessoas.filter(alocacao__isnull=True))
    pessoas = pessoas.all()
    qs_json = serializers.serialize('json', pessoas)
    return render(request,'pessoas/pessoas_table.html',{'pessoas':pessoas})

@login_required(login_url='/auth-user/login-user')
def visualizarPessoa(request,codigo):
    pessoa = Pessoas.objects.get(id=codigo)
    return render(request,'pessoas/visualizar_pessoas.html',{'pessoa':pessoa})

@login_required(login_url='/auth-user/login-user')
def pessoasModalCadastrar(request):
    id = request.GET.get('id')
    pessoa = None
    cursos = None
    data = {}
    if id:
        pessoa = Pessoas.objects.get(id=id)
        cursos = CursoSerializer(pessoa.cursos, many=True)
        if cursos:
            data['pessoa'] = pessoa
            data['cursos'] = cursos.data
    return render(request,'pessoas/modal_cadastrar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def pessoasModalAlocar(request):
    pessoaIds = request.GET.getlist('checked_values[]')
    data = {}
    if pessoaIds:
        pessoas = Pessoas.objects.filter(id__in=pessoaIds).all()
        pessoas = PessoaSerializer(pessoas, many = True)
        data['pessoas'] = pessoas.data
        eventos = Evento.objects.filter(~Q(status="finalizado"))
        eventos = EventoSerializer(eventos, many=True)
        data['eventos'] = eventos.data
    return render(request,'pessoas/modal_alocar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def cursosSelect(request):
    cursos = Curso.objects.all()
    return render(request,'pessoas/cursos_select.html',{'cursos':cursos})

@login_required(login_url='/auth-user/login-user')
def eliminarPessoa(request,codigo):
    user = Pessoas.objects.get(id=codigo)
    user.delete()
    return redirect('/gerenciar-pessoas')

# FIM PESSOAS