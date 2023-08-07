from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
import json
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def saveImagem(request):
    payload = json.loads(request.body)
    galeria_id = payload.pop('imagem_id', None)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/imagens/' + str(galeria_id) if galeria_id else 'http://localhost:8000/imagens'
    body = payload
    response = None
    error = None
    if galeria_id:
        response = requests.put(url, json=body, headers=headers)
    else:
        response = requests.post(url, json=body, headers=headers)
    return JsonResponse({'status': response.status_code, 'content': response.content.decode()})


@login_required(login_url='/auth-user/login-user')
def deleteImagem(request, imagem_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/imagens/' + str(imagem_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse({'status': response.status_code, 'message': response.content.decode()})


