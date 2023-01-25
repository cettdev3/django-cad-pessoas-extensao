from django.shortcuts import render, redirect

from sistema.models.atividade import Atividade
from sistema.models.acao import Acao
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests
import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def atividadesTable(request):
    nome = request.GET.get('nome')
    acao_id = request.GET.get('acao_id')
    atividades = Atividade.objects
    if acao_id:
        atividades = atividades.filter(acao__id = acao_id)
    if nome:
        atividades = atividades.filter(
            Q(descricao__contains = nome) | 
            Q(tipoAtividade__nome__contains = nome)
        )

    atividades = atividades.all()
    print(atividades)
    return render(request,'atividades/atividadesTabela.html',{'atividades':atividades})

@login_required(login_url='/auth-user/login-user')
def atividadeModal(request):
    acao_id = request.GET.get('acao_id')
    data = {}
    if acao_id:
        acao = Acao.objects.get(id=acao_id)
        data['acao'] = acao
    return render(request,'atividades/atividadesModal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarAtividade(request, codigo):
    atividade = Atividade.objects.get(id=codigo)
    atividade.delete()
    return JsonResponse({"message": "Deletado com sucesso"}, status=status.HTTP_200_OK)

@login_required(login_url='/auth-user/login-user')
def saveAtividade(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/atividades', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarAtividade(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/atividades/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def atividadeEditarModal(request, codigo):
    id = request.GET.get('id')
    atividade = Atividade.objects.get(id=codigo)
    return render(request,'atividades/atividadesModal.html',{"atividade":atividade})
