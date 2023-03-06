from django.shortcuts import render, redirect
from sistema.models.pessoa import Pessoas
from sistema.models.acao import Acao
from sistema.models.cidade import Cidade
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.escola import Escola
from sistema.services.camunda import CamundaAPI
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.serializers.acaoSerializer import AcaoSerializer
from sistema.serializers.escolaSerializer import EscolaSerializer
from django.db.models import Prefetch

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
    tipo = request.GET.get('tipo')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    order_by = request.GET.get('order_by')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}

    acaoResponse = requests.get('http://localhost:8000/acoes', params= {
        'tipo': tipo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'order_by': order_by,
    }, headers=headers)
    acaoResponseStatusCode = acaoResponse.status_code
    acaoResponse = json.loads(acaoResponse.content.decode())
    
    acoes = acaoResponse
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
    escolas = Escola.objects.all()
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    data['ct_emprestimo'] = Acao.EMPRESTIMO
    if id:
        acao = Acao.objects.get(id=id)
        data['acao'] = AcaoSerializer(acao).data 
    return render(request,'acoes/acoes_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarAcao(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    
    acaoResponse = requests.delete('http://localhost:8000/acoes/'+str(codigo), headers=headers)
    acaoResponseStatusCode = acaoResponse.status_code
    acaoResponse = json.loads(acaoResponse.content.decode())

    return redirect('/gerencia_acoes')

@login_required(login_url='/auth-user/login-user')
def saveAcao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    acaoData = json.loads(request.body)['data']
    itinerarios = json.loads(request.body)['itinerarios']
    acaoResponse = requests.post(
        'http://localhost:8000/acoes', 
        json={"acao": acaoData, "itinerarios": itinerarios}, 
        headers=headers
    )
    acaoResponseStatusCode = acaoResponse.status_code
    acaoResponse = json.loads(acaoResponse.content.decode())
    acao = Acao.objects.get(id=acaoResponse['id'])

    if acao.tipo in Acao.MAPPED_TIPOS:
        dados = {
            "variables": {
                "processDescription": {"value": acao.tipo + ", " + acao.cidade.nome, "type": "String"},
                "acao_id": {"value": acao.id, "type": "String"},
                "extrato": {"value": acao.extrato, "type": "String"},
            },
            "withVariablesInReturn": True
        }

        camunda = CamundaAPI()
        camundaResponse = camunda.startProcess("ProcessoDeEmprestimoDeIntensProcess",dados)
        acao.process_instance = camundaResponse['id']
        if acao.tipo == Acao.EMPRESTIMO:
            acao.status = Acao.STATUS_WAITING_TICKET
        acao.save()

    return JsonResponse(acaoResponse, status=acaoResponseStatusCode)

@login_required(login_url='/auth-user/login-user')
def editarAcao(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/acoes/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def acoesSelect(request):
    acoes = Acao.objects.all()
    return render(request,'acoes/acoes_select.html',{'acoes':acoes})

@login_required(login_url='/auth-user/login-user')
def visualizarAcao(request,codigo):
    acao = Acao.objects.prefetch_related(
        Prefetch(
            "membroexecucao_set", 
            queryset=MembroExecucao.objects
            .select_related("itinerario")
            .prefetch_related("itinerario__itinerarioitem_set")
        ),
    ).get(id=codigo)
    page_title = acao.descricao
    path_back = "gerencia_acoes"
    acao = AcaoSerializer(acao).data
    return render(request,'acoes/visualizar_acao.html',{
        'acao':acao, 
        'page_title': page_title,
        'path_back': path_back
    })