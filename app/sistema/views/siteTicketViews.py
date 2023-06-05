
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.ticket import Ticket
from sistema.models.escola import Escola
from sistema.models.atividade import Atividade
from sistema.models.anexo import Anexo
from sistema.models.alocacao import Alocacao
from sistema.models.dpEvento import DpEvento
from sistema.models.pessoa import Pessoas
from ..serializers.escolaSerializer import EscolaSerializer
import datetime
from django.utils import timezone
import ntplib

@login_required(login_url='/auth-user/login-user')
def ticketModal(request):
    id = request.GET.get('id')
    layout = request.GET.get('layout')
    model = request.GET.get('model')
    ticket = None
    data = {}
    if request.GET.get('membro_execucao_id') and model == 'membro_execucao':
        membroExecucao = MembroExecucao.objects.get(id=request.GET.get('membro_execucao_id'))
        parent_entity = membroExecucao.evento
        data['membroExecucao'] = membroExecucao
        data['evento'] = parent_entity
        data['beneficiario_id'] = membroExecucao.pessoa.id
    if request.GET.get('alocacao_id'):
        alocacao = Alocacao.objects.get(id=request.GET.get('alocacao_id'))
        acaoEnsino = alocacao.acaoEnsino
        data['alocacao'] = alocacao
        data['acaoEnsino'] = acaoEnsino
        data['beneficiario_id'] = alocacao.professor.id
    if request.GET.get('pessoa_id') and model == 'pessoa':
        pessoa = Pessoas.objects.get(id=request.GET.get('pessoa_id'))
        data['entity'] = pessoa
        data['parent_entity'] = None
    if request.GET.get('atividade_id') and model == 'atividade':
        atividade = Atividade.objects.get(id=request.GET.get('atividade_id'))
        data['entity'] = atividade
        parent_entity = atividade.evento
        data['parent_entity'] = parent_entity
    if id:
        ticket = ticket.objects.get(id=id)
        data['ticket'] = ticket
    if layout:
        data['layout'] = layout
    if model:
        data['model'] = model
    escolas = Escola.objects.all()
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    return render(request,'tickets/ticket_modal.html',data)


@login_required(login_url='/auth-user/login-user')
def ticketModalEdit(request, ticket_id):
    layout = request.GET.get('layout')
    data = {}
    model = request.GET.get('model')
    ticket = Ticket.objects.get(id=ticket_id)
    data['ticket'] = ticket
    data['model'] = model   
    escolas = Escola.objects.all()
    anexos = Anexo.objects.filter(model='ticket', id_model=ticket_id)
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    data['anexos'] = anexos
    return render(request,'tickets/ticket_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def ticket_form(request):
    form_id = request.GET.get('form_id')
    id = request.GET.get('id')
    evento_id = request.GET.get('evento_id') if request.GET.get('evento_id') else request.GET.get('dp_evento_id')
    model = request.GET.get('model')
    context = {}
    if form_id:
        context['form_id'] = form_id
    if id:
        ticket = Ticket.objects.get(id=id)
        context['ticket'] = ticket
    if evento_id:
        context['evento'] = DpEvento.objects.get(id=evento_id)
        context['parent_entity'] = DpEvento.objects.get(id=evento_id)
    if model:
        context['model'] = model

    return render(request,'tickets/ticket_form_collapsable.html', context)

@login_required(login_url='/auth-user/login-user')
def ticket_form_collapsable(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    solicitante = None
    try:
        solicitante = Pessoas.objects.get(user__id=request.user.id)
    except:
        return JsonResponse({'error': 'Para fazer solicitações você precisa estar vinculado a um usuario do sistema'}, status=400)
    solicitante = Pessoas.objects.get(user__id=request.user.id)
    tmz = timezone.get_current_timezone()
    dataCriacao = datetime.datetime.now(tz=tmz)
    body['solicitante_id'] = solicitante.id
    body['data_criacao'] = dataCriacao.strftime("%Y-%m-%dT%H:%M:%S%z")
    response = requests.post('http://localhost:8000/tickets', json=body, headers=headers)
    context = {}

    context['ticket'] = json.loads(response.content)
    context['atividade_id'] = body.get('atividade_id')
    context['evento_id'] = body.get('evento_id')
    
    return render(request,'tickets/ticket_form_collapsable_atividade.html', context)

@login_required(login_url='/auth-user/login-user')
def saveTicket(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.post('http://localhost:8000/tickets', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarTicket(request, ticket_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/tickets/'+ticket_id, json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

# rota de update criada especificamente para o ticket de atividade
@login_required(login_url='/auth-user/login-user')
def updateTicket(request, ticket_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.put('http://localhost:8000/tickets/'+ticket_id, json=body, headers=headers)
    context = {}
    context['ticket'] = json.loads(response.content)
    ticket = context.get('ticket')
    if ticket:
        atividade = ticket.get('atividade')
        if atividade:
            context['atividade_id'] = atividade.get('id')
            evento = atividade.get('evento')
            if evento:
                context['evento_id'] = evento.get('id')
    
    return render(request,'tickets/ticket_form_collapsable_atividade.html', context)

@login_required(login_url='/auth-user/login-user')
def eliminarTicket(request, ticket_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/tickets/' + str(ticket_id), headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)
