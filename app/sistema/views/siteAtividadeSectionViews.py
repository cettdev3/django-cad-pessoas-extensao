from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json
from rest_framework.authtoken.models import Token
from sistema.models.atividadeSection import AtividadeSection
from sistema.serializers.atividadeSectionSerializer import AtividadeSectionSerializer


@login_required(login_url='/auth-user/login-user')
def atividadeSectionModal(request):
    atividade_section_id = request.GET.get('atividade_section_id')
    dp_evento_id = request.GET.get('dp_evento_id')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/atividade-section/' + str(atividade_section_id) if atividade_section_id else 'http://localhost:8000/atividade-section/'
    response = requests.get(url, headers=headers)
    atividade_section = json.loads(response.content)
    return render(
        request,
        'atividades/atividadeSection/modal_atividade_section.html',
        {'atividade_section': atividade_section, 'dp_evento_id': dp_evento_id}
    )

@login_required(login_url='/auth-user/login-user')
def atividadeSectionTable(request):
    evento_id = request.GET.get('evento_id')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get(
        'http://localhost:8000/atividade-section',
        params={
            'evento_id': evento_id
        },
        headers=headers
    )
    atividadeSections = json.loads(response.content)
    return render(
        request,
        'atividades/atividadeSection/atividade-section-table.html',
        {'atividadeSections': atividadeSections, 'evento_id': evento_id}
    )

@login_required(login_url='/auth-user/login-user')
def saveAtividadeSection(request):
    payload = json.loads(request.body)
    atividade_section_id = payload.pop('atividade_section_id', None)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    urlId = "/"+str(atividade_section_id) if atividade_section_id else ""
    url = 'http://localhost:8000/atividade-section' + urlId
    body = payload
    response = None
    fromCreate = False
    if atividade_section_id:
        response = requests.put(url, json=body, headers=headers)
    else:
        response = requests.post(url, json=body, headers=headers)
        fromCreate = True
    atividadeSection = json.loads(response.content.decode())

    return render(
        request,
        'atividades/atividadeSection/atividade-section-item.html',
        {
            'atividadeSection': atividadeSection,
            'fromCreate': fromCreate
        }
    )

@login_required(login_url='/auth-user/login-user')
def updateAtividadeSection(request, atividade_section_id):
    payload = json.loads(request.body)
    atividade_section_id = payload.pop('atividade_section_id', None)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key} 
    url = 'http://localhost:8000/atividade-section' + "/"+str(atividade_section_id)
    body = payload
    response = requests.put(url, json=body, headers=headers)
    
    atividadeSection = json.loads(response.content.decode())

    return JsonResponse({'data': atividadeSection})

@login_required(login_url='/auth-user/login-user')
def deleteAtividadeSection(request, atividade_section_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/atividade-section/' + str(atividade_section_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})

@login_required(login_url='/auth-user/login-user')
def atividadeSectionComponent(request, atividade_section_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/atividade-section/' + str(atividade_section_id)
    response = requests.get(url, headers=headers)
    atividade_section = response.json()
    return render(
        request,
        'atividades/componentes/atividade-section-component.html',
        {'atividade_section': atividade_section}
    )