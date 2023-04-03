
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.ticket import Ticket
from sistema.models.dpEvento import DpEvento

@login_required(login_url='/auth-user/login-user')
def ticketModal(request):
    print("ticket_form")
    print(request.GET)
    id = request.GET.get('id')
    layout = request.GET.get('layout')
    ticket = None
    data = {}
    if request.GET.get('membro_execucao_id'):
        membroExecucao = MembroExecucao.objects.get(id=request.GET.get('membro_execucao_id'))
        evento = membroExecucao.evento
        data['membro_execucao'] = membroExecucao
        data['evento'] = evento
    if id:
        ticket = ticket.objects.get(id=id)
        data['ticket'] = ticket
    if layout:
        data['layout'] = layout
    return render(request,'tickets/ticket_modal.html',data)

def ticketModalEdit(request, ticket_id):
    print("ticket_form")
    print(request.GET)
    layout = request.GET.get('layout')
    data = {}
    ticket = Ticket.objects.get(id=ticket_id)
    data['ticket'] = ticket
    data['evento'] = ticket.membro_execucao.evento
    if layout:
        data['layout'] = layout
    return render(request,'tickets/ticket_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def ticket_form(request):
    form_id = request.GET.get('form_id')
    id = request.GET.get('id')
    evento_id = request.GET.get('evento_id')
    context = {}
    if form_id:
        context['form_id'] = form_id
    if id:
        ticket = Ticket.objects.get(id=id)
        context['ticket'] = ticket
    if evento_id:
        context['evento'] = DpEvento.objects.get(id=evento_id)

    return render(request,'tickets/ticket_form_collapsable.html', context)

@login_required(login_url='/auth-user/login-user')
def saveTicket(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print(body)
    response = requests.post('http://localhost:8000/tickets', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarTicket(request, ticket_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print(body)
    response = requests.put('http://localhost:8000/tickets/'+ticket_id, json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarTicket(request, ticket_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/tickets/' + str(ticket_id), headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)
