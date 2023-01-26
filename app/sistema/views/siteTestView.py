from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.alocacaoSerializer import AlocacaoSerializer
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.serializers.pessoaSerializer import PessoaSerializer
from sistema.serializers.eventoSerializer import EventoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.alocacao import Alocacao
from sistema.models.curso import Curso
from sistema.models.ensino import Ensino
from sistema.models.escola import Escola
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Q, Exists
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

@login_required(login_url='/auth-user/login-user')
def testeForm(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/alocacoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def testeSave(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/alocacoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def testeEdit(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/alocacoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def testeModal(request):
    # buscar apenas 1 id para editar
    data = {}
    eventos = Ensino.objects.filter(~Q(status="finalizado"))
    eventos = EventoSerializer(eventos, many=True)
    data['eventos'] = eventos.data

    alocacao_id = request.GET.get('alocacao_id')
    if alocacao_id:
        alocacao = Alocacao.objects.get(id=alocacao_id)
        data["alocacao"] = AlocacaoSerializer(alocacao).data
        return render(request,'teste/testeModal.html', data)
    # buscar pessoas para alocar
    pessoaIds = request.GET.getlist('checked_values[]')
    if pessoaIds:
        pessoas = Pessoas.objects.filter(id__in=pessoaIds).all()
        pessoas = PessoaSerializer(pessoas, many = True)
        data['pessoas'] = pessoas.data
        return render(request,'teste/testeModal.html',data)

    return render(request, 'teste/testeModal.html')

@login_required(login_url='/auth-user/login-user')
def testeGerenciar(request): 
    return render(request,'teste/testeGerenciar.html')

@login_required(login_url='/auth-user/login-user')
def testeTabela(request):
    nome = request.GET.get('nome')
    escolas = Escola.objects
    if nome:
        escolas = escolas.filter(nome__contains = nome)
    escolas = escolas.all()
    return render(request,'teste/testeTabela.html', {'escolas': escolas})
