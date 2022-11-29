from django.shortcuts import render, redirect
from sistema.models.turno import Turno
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def gerencia_turnos(request):
    page_title = "Turnos"
    count = 0
    turnos = Turno.objects.all()
    for p in turnos:
        count += 1

    return render(request,'turnos/gerenciar_turnos.html',
    {'turnos':turnos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def turnoTable(request):
    nome = request.GET.get('nome')
    turnos = Turno.objects
    if nome:
        turnos = turnos.filter(nome__contains = nome)
    turnos = turnos.all()
    return render(request,'turnos/turnos_tabela.html',{'turnos':turnos})

@login_required(login_url='/auth-user/login-user')
def visualizarTurno(request,codigo):
    turno = Turno.objects.get(id=codigo)
    return render(request,'turnos/visualizar_turno.html',{'turno':turno})

@login_required(login_url='/auth-user/login-user')
def turnoModal(request):
    id = request.GET.get('id')
    turno = None
    data = {}
    if id:
        turno = Turno.objects.get(id=id)
        data['turno'] = turno
    return render(request,'turnos/turnos_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarTurno(request,codigo):
    turno = Turno.objects.get(id=codigo)
    turno.delete()
    return redirect('/gerencia_turnos')

@login_required(login_url='/auth-user/login-user')
def saveTurno(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/turnos', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarTurno(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/turnos/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def turnosSelect(request):
    turnos = Turno.objects.all()
    return render(request,'turnos/turnos_select.html',{'turnos':turnos})

@login_required(login_url='/auth-user/login-user')
def turnoForm(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/alocacoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)