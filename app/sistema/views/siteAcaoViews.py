from django.shortcuts import render, redirect
from sistema.models.pessoa import Pessoas
from sistema.models.acao import Acao
from sistema.models.cidade import Cidade
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def gerencia_acoes(request):
    page_title = "Ações"
    count = 0
    acoes = Acao.objects.all()
    for p in acoes:
        count += 1
    
    return render(request,'acoes/gerenciar_acoes.html',
    {'acoes':acoes,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def acaoTable(request):
    nome = request.GET.get('nome')
    acoes = Acao.objects
    if nome:
        acoes = acoes.filter(nome__contains = nome)
    acoes = acoes.all()
    return render(request,'acoes/acoes_tabela.html',{'acoes':acoes})

@login_required(login_url='/auth-user/login-user')
def visualizarAcao(request,codigo):
    acao = Acao.objects.get(id=codigo)
    return render(request,'acoes/visualizar_acao.html',{'acao':acao})

@login_required(login_url='/auth-user/login-user')
def acaoModal(request):
    id = request.GET.get('id')
    acao = None
    data = {}
    if id:
        acao = Acao.objects.get(id=id)
        data['acao'] = acao
    return render(request,'acoes/acoes_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarAcao(request,codigo):
    acao = Acao.objects.get(id=codigo)
    acao.delete()
    return redirect('/gerencia_acoes')

@login_required(login_url='/auth-user/login-user')
def saveAcao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/acoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarAcao(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print(body)
    response = requests.put('http://localhost:8000/acoes/'+str(codigo), json=body, headers=headers)
    # print(response.content)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def acoesSelect(request):
    acoes = Acao.objects.all()
    return render(request,'acoes/acoes_select.html',{'acoes':acoes})

@login_required(login_url='/auth-user/login-user')
def acaoForm(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/acoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def pessoaTicketForm(request):
    data = {}
    data['id_to_remove'] = int(request.GET.get('id')) 
    data['id_to_add'] = int(request.GET.get('id')) + 1
    data['hide_remove_button'] = "hide" if data["id_to_remove"] == 0 else "" 
    data['pessoas'] = Pessoas.objects.all()
    data['cidades'] = Cidade.objects.all()
    return render(request,'acoes/pessoa_ticket_form.html',data)