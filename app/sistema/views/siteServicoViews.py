from django.shortcuts import render, redirect
from sistema.models.servico import Servico
from sistema.models.atividade import Atividade
from sistema.serializers.atividadeSerializer import AtividadeSerializer
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def ServicoModalCadastrar(request):
    servico_id = request.GET.get('servico_id')
    atividade_id = request.GET.get('atividade_id')
    servico = None
    data = {}
    if servico_id:
        servico = Servico.objects.get(id=servico_id)
        data['servico'] = servico
        
    if atividade_id:
        atividade = Atividade.objects.select_related("cidade").filter(id=atividade_id).first()
        data['atividade'] =  AtividadeSerializer(atividade).data
    else:
        return JsonResponse({'error': 'atividade_id not found'}, status=400) 
    return render(request,'servicos/servicoModal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarServico(request,codigo):
    servico = Servico.objects.get(id=codigo)
    servico.delete()
    return JsonResponse({'success': 'servico deleted'}, status=200)

@login_required(login_url='/auth-user/login-user')
def saveServico(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.post('http://localhost:8000/servicos', json=body, headers=headers)
    return render(request,'servicos/servico-row.html',{'servico':json.loads(response.content), 'fromCreate': True})

@login_required(login_url='/auth-user/login-user')
def editarServico(request, servico_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)
    response = requests.put('http://localhost:8000/servicos/'+str(servico_id), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def getServicos(request):
    atividade_id = request.GET.get('atividade_id')
    token = Token.objects.get(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body =  {'atividade_id': atividade_id}
    response = requests.get('http://localhost:8000/servicos', json=body, headers=headers)
    servicos = json.loads(response.content)
    return render(request,'servicos/servicos-table.html',{'servicos':servicos})