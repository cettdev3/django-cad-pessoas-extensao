
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.ticket import Ticket

@login_required(login_url='/auth-user/login-user')
def ticketModal(request):
    id = request.GET.get('id')
    ticket = None
    data = {}
    if request.GET.get('membro_execucao_id'):
        membroExecucao = MembroExecucao.objects.get(id=request.GET.get('membro_execucao_id'))
        data['membro_execucao_id'] = request.GET.get('membro_execucao_id')
        data['tipo'] = membroExecucao.tipo
        data['nome'] = membroExecucao.pessoa.nome
        data['data_inicio'] = membroExecucao.data_inicio
        data['data_fim'] = membroExecucao.data_fim
        fromTable = request.GET.get('from')
        data['nome_escola'] =  membroExecucao.acao.escola.nome if fromTable == 'acao' else membroExecucao.evento.escola.nome
        data['endereco_completo'] = membroExecucao.endereco_completo
    if id:
        ticket = ticket.objects.get(id=id)
        data['ticket'] = ticket
    return render(request,'tickets/ticket_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def ticket_form(request):
    form_id = request.GET.get('form_id')
    id = request.GET.get('id')
    context = {}
    if form_id:
        context['form_id'] = form_id
    if id:
        ticket = Ticket.objects.get(id=id)
        context['ticket'] = ticket

    return render(request,'tickets/ticket_form.html', context)

@login_required(login_url='/auth-user/login-user')
def saveTicket(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print(body)
    response = requests.post('http://localhost:8000/tickets', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)
