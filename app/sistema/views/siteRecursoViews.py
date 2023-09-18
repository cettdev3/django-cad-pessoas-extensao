from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

baseUrl = 'http://localhost:8000/recursos'

@login_required(login_url='/auth-user/login-user')
def recursoForm(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = baseUrl
    if request.GET.get('model_id'):
        url += "/"+request.GET.get('model_id')
        response = requests.get(url, params={}, headers=headers)
        return render(request,'recursos/recursoForm.html', {'recurso': json.loads(response.content)})
    return render(request,'recursos/recursoForm.html')

@login_required(login_url='/auth-user/login-user')
def recursoSave(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.post(baseUrl, json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def recursoEdit(request, recurso_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.put(baseUrl + '/' + str(recurso_id), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def recursoTabela(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    params = {}
    if request.GET.get('evento_id'):
        params['evento_id'] = request.GET.get('evento_id')
    if request.GET.get('proposta_projeto_id'):
        params['proposta_projeto_id'] = request.GET.get('proposta_projeto_id')
    response = requests.get(baseUrl, params=params, headers=headers)
    recursos = json.loads(response.content)
    return render(request,'recursos/recursoTable.html', {'recursos': recursos})

@login_required(login_url='/auth-user/login-user')
def recursoDelete(request, recursos_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete(baseUrl + '/' + str(recursos_id), headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)