from django.shortcuts import render, redirect
from sistema.models.dpEvento import DpEvento
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.escola import Escola
from sistema.models.ensino import Ensino
from sistema.services.camunda import CamundaAPI
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.serializers.dpEventoSerializer import DpEventoSerializer
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.serializers.escolaSerializer import EscolaSerializer
from django.db.models import Prefetch

@login_required(login_url='/auth-user/login-user')
def gerencia_dp_eventos(request):
    page_title = "Eventos"
    count = 0
    dp_eventos = DpEvento.objects.all()
    for p in dp_eventos:
        count += 1
    
    return render(request,'dpEventos/gerenciar_dp_eventos.html',
    {'dp_eventos':dp_eventos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def dpEventoTable(request):
    tipo = request.GET.get('tipo')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = {"tipo": tipo}

    dpEventoResponse = requests.get('http://localhost:8000/dp-eventos', json=body, headers=headers)
    dpEventoResponseStatusCode = dpEventoResponse.status_code
    dpEventoResponse = json.loads(dpEventoResponse.content.decode())
    
    dpEventos = dpEventoResponse
    return render(request,'dpEventos/dp_eventos_tabela.html',{'dpEventos':dpEventos})

@login_required(login_url='/auth-user/login-user')
def dpEventoModal(request):
    id = request.GET.get('id')
    dpEvento = None
    data = {}
    escolas = Escola.objects.all()
    ensinos = Ensino.objects.all()
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    data['ensinos'] = EnsinoSerializer(ensinos, many=True).data
    data['ct_emprestimo'] = DpEvento.EMPRESTIMO
    if id:
        dpEvento = DpEvento.objects.get(id=id)
        data['dpEvento'] = DpEventoSerializer(dpEvento).data 
    return render(request,'dpEventos/dp_eventos_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarDpEvento(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    
    dpEventoResponse = requests.delete('http://localhost:8000/dp-eventos/'+str(codigo), headers=headers)
    dpEventoResponseStatusCode = dpEventoResponse.status_code
    dpEventoResponse = json.loads(dpEventoResponse.content.decode())

    return redirect('/gerencia_dp_eventos')

@login_required(login_url='/auth-user/login-user')
def saveDpEvento(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    dpEventoData = json.loads(request.body)['data']
    itinerarios = json.loads(request.body)['itinerarios']
    dpEventoResponse = requests.post(
        'http://localhost:8000/dp-eventos', 
        json={"dpEvento": dpEventoData, "itinerarios": itinerarios}, 
        headers=headers
    )
    dpEventoResponseStatusCode = dpEventoResponse.status_code
    dpEventoResponse = json.loads(dpEventoResponse.content.decode())
    dpEvento = DpEvento.objects.get(id=dpEventoResponse['id'])

    if dpEvento.tipo in DpEvento.MAPPED_TIPOS:
        dados = {
            "variables": {
                "processDescription": {"value": dpEvento.tipo + ", " + dpEvento.cidade.nome, "type": "String"},
                "dpEvento_id": {"value": dpEvento.id, "type": "String"},
                "extrato": {"value": dpEvento.extrato, "type": "String"},
            },
            "withVariablesInReturn": True
        }

        camunda = CamundaAPI()
        camundaResponse = camunda.startProcess("ProcessoDeEmprestimoDeIntensProcess",dados)
        dpEvento.process_instance = camundaResponse['id']
        if dpEvento.tipo == DpEvento.EMPRESTIMO:
            dpEvento.status = DpEvento.STATUS_WAITING_TICKET
        dpEvento.save()

    return JsonResponse(dpEventoResponse, status=dpEventoResponseStatusCode)

@login_required(login_url='/auth-user/login-user')
def editarDpEvento(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/dp-eventos/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def dp_eventosSelect(request):
    dp_eventos = DpEvento.objects.all()
    return render(request,'dpEventos/dp-eventos_select.html',{'dp_eventos':dp_eventos})

@login_required(login_url='/auth-user/login-user')
def visualizarDpEvento(request,codigo):
    dpEvento = DpEvento.objects.prefetch_related(
        Prefetch(
            "membroexecucao_set", 
            queryset=MembroExecucao.objects
            .select_related("itinerario")
            .prefetch_related("itinerario__itinerarioitem_set")
        ),
    ).get(id=codigo)
    page_title = dpEvento.descricao
    path_back = "gerencia_dp_eventos"
    dpEvento = DpEventoSerializer(dpEvento).data
    return render(request,'dpEventos/visualizar_dp_evento.html',{
        'dpEvento':dpEvento, 
        'page_title': page_title,
        'path_back': path_back
    })