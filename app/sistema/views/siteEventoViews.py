from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.eventoSerializer import EventoSerializer
from sistema.serializers.escolaSerializer import EscolaSerializer
from sistema.models.curso import Curso
from sistema.models.endereco import Endereco
from sistema.models.escola import Escola
from sistema.models.cidade import Cidade
from sistema.models.evento import Evento
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def gerencia_eventos(request):
    page_title = "eventos"
    count = 0
    eventos = Evento.objects.all()
    for p in eventos:
        count += 1

    return render(request,'eventos/gerencia_eventos.html',
    {'eventos':eventos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def eventosTable(request):
    nome = request.GET.get('nome')
    eventos = Evento.objects
    if nome:
        eventos = eventos.filter(nome__contains = nome)
    eventos = eventos.all()
    return render(request,'eventos/eventos_table.html',{'eventos':eventos})

@login_required(login_url='/auth-user/login-user')
def visualizarEvento(request,codigo):
    evento = Evento.objects.get(id=codigo)
    page_title = evento.observacao
    path_back = "gerenciar-eventos"
    return render(request,'eventos/visualizar_evento.html',{
        'evento':evento, 
        'page_title': page_title,
        'path_back': path_back
    })

@login_required(login_url='/auth-user/login-user')
def eventosModalCadastrar(request):
    id = request.GET.get('id')
    evento = None
    escolas = Escola.objects.all()
    data = {}
    if id:
        evento = Evento.objects.get(id=id)
        data['evento'] = EventoSerializer(evento).data
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    return render(request,'eventos/modal_cadastrar_evento.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarEvento(request,codigo):
    evento = Evento.objects.get(id=codigo)
    evento.delete()
    return redirect('/gerenciar-eventos')

@login_required(login_url='/auth-user/login-user')
def saveEvento(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print(body)
    response = requests.post('http://localhost:8000/eventos', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarEvento(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/eventos/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)