from django.shortcuts import render, redirect
from sistema.models import Pessoas, Curso, Atividade, Cidade, MembroExecucao, OrcamentoItem, Orcamento
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from sistema.models import PropostaProjeto
from django.db import transaction
import requests
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.urls import reverse

# @login_required(login_url="/auth-user/login-user")
# def updateComentario(request, pk):
#     payload = json.loads(request.body)
#     token, created = Token.objects.get_or_create(user=request.user)
#     headers = {'Authorization': 'Token ' + token.key}
#     url = 'http://localhost:8000/comentarios/'+str(pk)
#     body = payload
#     response = requests.put(url, json=body, headers=headers)

#     comentario = json.loads(response.content)
#     return JsonResponse(comentario)

@login_required(login_url="/auth-user/login-user")
def createComentario(request):
    payload = json.loads(request.body)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/comentarios'
    body = payload
    response = requests.post(url, json=body, headers=headers)

    comentario = json.loads(response.content)
    return JsonResponse(comentario)

# @login_required(login_url="/auth-user/login-user")
# def removeComentario(request, pk):
#     token, created = Token.objects.get_or_create(user=request.user)
#     headers = {'Authorization': 'Token ' + token.key}
#     url = 'http://localhost:8000/comentarios/'+str(pk)
#     response = requests.delete(url, headers=headers)
#     return JsonResponse({"message": "Comentario removido com sucesso!"})