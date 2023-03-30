from django.shortcuts import render, redirect
from sistema.models.dataRemovida import DataRemovida
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def createDataRemovida(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    print("fsajhfadlskhf",request.body)
    body = json.loads(request.body)
    print(body)
    response = requests.post('http://localhost:8000/datas-removidas', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarDataRemovida(request, codigo):
    dataRemovida = DataRemovida.objects.get(id=codigo)
    dataRemovida.delete()
    return JsonResponse({"message": "Data removida eliminada com sucesso!"}, status=200)
