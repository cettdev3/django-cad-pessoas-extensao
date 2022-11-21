from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.alocacaoSerializer import AlocacaoSerializer
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.alocacao import Alocacao
from sistema.models.curso import Curso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

@login_required(login_url='/auth-user/login-user')
def alocacoesTable(request):
    print("dentro de alocacoes table")
    evento_id = request.GET.get('evento_id')
    print("eventoId: ", evento_id)
    alocacoes = Alocacao.objects
    if evento_id:
        alocacoes = alocacoes.filter(evento_id = evento_id)
    alocacoes = alocacoes.all()
    print(alocacoes)
    return render(request,'alocacoes/alocacoes_table.html',{'alocacoes':alocacoes})

@login_required(login_url='/auth-user/login-user')
def alocacaoForm(request):
    id = request.GET.get('alocacao_id')
    alocacao = None
    data = {}
    if id:
        alocacao = Alocacao.objects.get(id=id)
        data['alocacao'] = AlocacaoSerializer(alocacao).data
    if request.GET.get('formId'):
        data['formId'] = request.GET.get('formId')
    else :
        data['formId'] = 'alocacaoForm'
    return render(request,'alocacoes/form_alocacoes.html',data)

@login_required(login_url='/auth-user/login-user')
def alocacaoModalCadastrar(request):
    id = request.GET.get('id')
    alocacao = None
    data = {}
    if id:
        alocacao = Alocacao.objects.get(id=id)
        alocacao = AlocacaoSerializer(alocacao).data
        data['alocacao'] = alocacao
        print(data)
    return render(request,'alocacoes/modal_cadastrar_alocacao.html',data)

@login_required(login_url='/auth-user/login-user')
def saveAlocacao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/alocacoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarAlocacao(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    print(request.body)
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/alocacoes/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarAlocacao(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/alocacoes/'+str(codigo), headers=headers)
    
    return HttpResponse(status=response.status_code)
