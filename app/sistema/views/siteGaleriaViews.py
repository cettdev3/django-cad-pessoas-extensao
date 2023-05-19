from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json
from rest_framework.authtoken.models import Token
from sistema.models.galeria import Galeria
from sistema.serializers.galeriaSerializer import GaleriaSerializer


@login_required(login_url='/auth-user/login-user')
def galeriaModal(request):
    galeria_id = request.GET.get('galeria_id')
    dp_evento_id = request.GET.get('dp_evento_id')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/galerias/' + str(galeria_id) if galeria_id else 'http://localhost:8000/galerias'
    response = requests.get(url, headers=headers)
    galeria = json.loads(response.content)
    return render(
        request,
        'galerias/modal_galeria.html',
        {'galeria': galeria, 'dp_evento_id': dp_evento_id}
    )


@login_required(login_url='/auth-user/login-user')
def galeriaTable(request):
    dp_evento_id = request.GET.get('dp_evento_id')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get(
        'http://localhost:8000/galerias',
        params={
            'dp_evento_id': dp_evento_id
        },
        headers=headers
    )
    galerias = json.loads(response.content)
    return render(
        request,
        'galerias/galerias_table.html',
        {'galerias': galerias, 'dp_evento_id': dp_evento_id}
    )


@login_required(login_url='/auth-user/login-user')
def saveGaleria(request):
    payload = json.loads(request.body)
    galeria_id = payload.pop('galeria_id', None)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/galerias/' + str(galeria_id) if galeria_id else 'http://localhost:8000/galerias'
    body = payload
    response = None
    if galeria_id:
        response = requests.put(url, json=body, headers=headers)
    else:
        response = requests.post(url, json=body, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})


@login_required(login_url='/auth-user/login-user')
def deleteGaleria(request, galeria_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/galerias/' + str(galeria_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})


