from django.contrib.auth.decorators import login_required
import requests
from rest_framework.authtoken.models import Token
import json
from django.http import JsonResponse
from django.shortcuts import render

@login_required(login_url='/auth-user/login-user')
def getMembroExecucaoRoles(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    params = {
        'order_by': request.GET.get('order_by'),
    }

    response = requests.get('http://localhost:8000/membro-execucao-roles', params=params, headers=headers)
    return JsonResponse(json.loads(response.content.decode()),status=response.status_code, safe=False)

@login_required(login_url="/auth-user/login-user")
def getMembroExecucaoRoleForm(request):
    return render(
        request,
        "membroExecucaoRole/membroExecucaoRoleForm.html"
    )

@login_required(login_url="/auth-user/login-user")
def membroExecucaoRoleCreate(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.post('http://localhost:8000/membro-execucao-roles', json=body, headers=headers)
    return JsonResponse(json.loads(response.content.decode()),status=response.status_code, safe=False)
