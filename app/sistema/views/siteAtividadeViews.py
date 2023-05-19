from django.shortcuts import render, redirect

from sistema.models.atividade import Atividade
from sistema.models.acao import Acao
from sistema.models.atividadeSection import AtividadeSection
from sistema.models.dpEvento import DpEvento
from sistema.models.departamento import Departamento
from sistema.models.membroExecucao import MembroExecucao
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from ..serializers.atividadeSerializer import AtividadeSerializer
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
    evento_id = request.GET.get('dp_evento_id')
    atividades = Atividade.objects
    if acao_id:
        atividades = atividades.filter(acao__id = acao_id)
    if nome:
        atividades = atividades.filter(
            Q(descricao__contains = nome) | 
            Q(tipoAtividade__nome__contains = nome)
        )

    atividades = atividades.prefetch_related("servico_set").all()
    atividades = AtividadeSerializer(atividades, many=True).data
    return render(request,'atividades/atividadesTabela.html',{'atividades':atividades})

@login_required(login_url='/auth-user/login-user')
def atividadesDpEventoTable(request):
    nome = request.GET.get('nome')
    evento_id = request.GET.get('dp_evento_id')
    atividades = Atividade.objects
    if evento_id:
        atividades = atividades.filter(evento__id = evento_id)
    if nome:
        atividades = atividades.filter(
            Q(descricao__contains = nome) | 
            Q(tipoAtividade__nome__contains = nome)
        )
    atividadeSections = AtividadeSection.objects.filter(evento__id = evento_id).order_by("order").all()
    atividades = atividades.all()
    categorias = Atividade().CATEGORY_CHOICES

    data = {}
    data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id = evento_id).all()
    data['atividades'] = atividades,
    data['evento_id'] = evento_id
    data['atividadeSections'] = atividadeSections
    data['categorias'] = categorias
    data['departamentos'] = Departamento.objects.all()

    return render(request,'atividades/atividadesTabela.html', data)

@login_required(login_url='/auth-user/login-user')
def atividadeModal(request):
    acao_id = request.GET.get('acao_id')
    evento_id = request.GET.get('dp_evento_id')
    data = {}
    if acao_id:
        acao = Acao.objects.get(id=acao_id)
        data['acao'] = acao
    if evento_id:
        evento = DpEvento.objects.get(id=evento_id)
        data['evento'] = evento
    return render(request,'atividades/atividadesModal.html',data)

@login_required(login_url='/auth-user/login-user')
def deleteAtividade(request, atividade_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/atividades/' + str(atividade_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})

@login_required(login_url='/auth-user/login-user')
def saveAtividade(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.post('http://localhost:8000/atividades', json=body, headers=headers)
    atividade = json.loads(response.content)
    categorias = Atividade().CATEGORY_CHOICES
    thumbnailStyle = True

    data = {}
    eventoId = atividade.get("evento").get("id")
    data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id = eventoId).all()
    data['atividade'] = atividade
    data['evento_id'] = eventoId
    data['categorias'] = categorias
    data['thumbnailStyle'] = thumbnailStyle
    data['fromCreate'] = True
    data['departamentos'] = Departamento.objects.all()
    return render(request,'atividades/atividade-row.html',data)

@login_required(login_url='/auth-user/login-user')
def editarAtividade(request, atividade_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    template = body.get('template') if body.get('template') else "atividade-row.html"
    response = requests.put('http://localhost:8000/atividades/'+str(atividade_id), json=body, headers=headers)
    atividade = json.loads(response.content)
    categorias = Atividade().CATEGORY_CHOICES
    thumbnailStyle = True
    data = {}
    # "atividade":atividade, "fromCreate": True, "categorias":categorias, "thumbnailStyle":thumbnailStyle
    eventoId = atividade.get("evento").get("id")
    data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id = eventoId).all()
    data['atividade'] = atividade
    data['evento_id'] = eventoId
    data['categorias'] = categorias
    data['thumbnailStyle'] = thumbnailStyle
    data['departamentos'] = Departamento.objects.all()
    return render(request,'atividades/'+template,data)

@login_required(login_url='/auth-user/login-user')
def getAtividadeDrawer(request, atividade_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/atividades/'+str(atividade_id), headers=headers)
    atividade = json.loads(response.content)
    categorias = Atividade().CATEGORY_CHOICES
    thumbnailStyle = True

    return render(request,'atividades/atividade-drawer.html',{
        "atividade":atividade, 
        "categorias":categorias, 
        "thumbnailStyle":thumbnailStyle
    })