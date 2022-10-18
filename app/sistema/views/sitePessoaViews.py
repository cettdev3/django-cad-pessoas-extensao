from contextlib import redirect_stderr
from pyexpat.errors import messages
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
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_pessoas(request):
    page_title = "Pessoas"
    count = 0
    pessoa = Pessoas.objects.all()
    print('-------------------------\n\n'+str(pessoa))
    for p in pessoa:
        count += 1

    return render(request,'pessoas/gerencia_pessoas.html',
    {'pessoas':pessoa,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def pessoasTable(request):
    nome = request.GET.get('nome')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    pessoas = Pessoas.objects
    if nome:
        pessoas = pessoas.filter(nome__contains = nome)
    if data_fim and data_inicio:
        print("filtrando")
        pessoas = pessoas.filter(
            Q(alocacao__data_inicio__lt=data_inicio,
            alocacao__data_fim__lt=data_inicio) | 
            Q(alocacao__data_inicio__gt=data_fim,
            alocacao__data_fim__gt=data_fim) | 
            Q(alocacao__evento__status__in=["finalizado", "adiado"]) |
            Q(alocacao__isnull=True)
        )
    pessoas = pessoas.all()
    qs_json = serializers.serialize('json', pessoas)
    print(qs_json)
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
        print(cursos)
        if cursos:
            data['pessoa'] = pessoa
            data['cursos'] = cursos.data
    return render(request,'pessoas/modal_cadastrar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def pessoasModalAlocar(request):
    pessoaIds = request.GET.getlist('checked_values[]')
    data = {}
    print("ids da requisicao",pessoaIds)
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


[
    {"model": 
    "sistema.pessoas", "pk": 86, "fields": 
    {"email": 
    "jose@email", "nome": 
    "jose da silva", "data_nascimento": 
    "2000-03-15", "telefone": 
    "(62)9 8585-8585", "cpf": 
    "458.745.874-77", "rg": 
    "45587.45", "orgao_emissor": 
    "SSP-GO", "cargo": 
    "professor", "banco": 
    "Itau", "agencia": 
    "4587445", "conta": 
    "45878546454", "pix": 
    "454654987789", "tipo": 
    "clt", 
"qtd_contratacoes": 
"0", "user_camunda": 
"", "cidade": 
"Goiania", "bairro": 
"Coiembra", "rua": 
"Rua 250", "cep": 
"75.386-222", "complemento": 
"casa 4", "cursos": [4]}}, 
{"model": 
"sistema.pessoas", "pk": 87, "fields": {"email": 
"maria@email", "nome": 
"maria da silva", "data_nascimento": 
"1995-04-15", "telefone": 
"(62)9 8555-5555", "cpf": 
"454.478.784-54", "rg": 
"45646.54", "orgao_emissor": 
"SSP-GO", "cargo": 
"professor", "banco": 
"Brasdesco", "agencia": 
"44558888", "conta": 
"554456646", "pix": 
"4564654694", "tipo": 
"clt", "qtd_contratacoes": 
"0", "user_camunda": 
"", "cidade": 
"Trindade", "bairro": 
"Setor Garavelo", 
"rua": 
"Rua  10", "cep": 
"12.545-887", "complemento": 
"Casa amarela", "cursos": [4, 5]}}, 
{"model": 
"sistema.pessoas", "pk": 89, "fields": {"email": 
"sfas", "nome": 
"sem alocacao", "data_nascimento": 
"2022-10-14", "telefone": 
"(01)3 2645-6464", "cpf": 
"456.545.646-45", "rg": 
"46464.65", "orgao_emissor": 
"SSP-GO", "cargo": 
"estoquista", "banco": 
"fsaf", "agencia": 
"fsdf", "conta": 
"dfsfas", "pix": 
"dfdsf", "tipo": 
"rpa", "qtd_contratacoes": 
"0", "user_camunda": 
"sdfsd", "cidade": 
"safsd", "bairro": 
"afsdf", "rua": 
"sfsdf", "cep": 
"54.646-546", "complemento": 
"44464", "cursos": [4, 5]}}]