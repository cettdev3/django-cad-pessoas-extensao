from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.pessoa import Pessoas
from sistema.models.cidade import Cidade
from sistema.models.acao import Acao
from sistema.models.dpEvento import DpEvento
from sistema.models.atividade import Atividade
from django.contrib.auth.decorators import login_required
import requests
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from django.http import JsonResponse

@login_required(login_url='/auth-user/login-user')
def membrosExecucaoTable(request):
    acao_id = request.GET.get('acao_id')
    membros_execucao = MembroExecucao.objects.prefetch_related('ticket_set')
    if acao_id:
        membros_execucao = membros_execucao.filter(acao_id = acao_id)
    membros_execucao = membros_execucao.all()
    serializer = MembroExecucaoSerializer(membros_execucao, many=True)
    return render(
        request,
        'membrosExecucao/membros_execucao_table.html',
        {'membros_execucao':serializer.data}
    )

@login_required(login_url='/auth-user/login-user')
def membrosExecucaoDpEventoTable(request):
    evento_id = request.GET.get('dp_evento_id')
    membros_execucao = MembroExecucao.objects.prefetch_related('ticket_set')
    if evento_id:
        membros_execucao = membros_execucao.filter(evento_id = evento_id)
    membros_execucao = membros_execucao.all()
    dp_eventos = DpEvento.objects.prefetch_related('membroexecucao_set').get(id=evento_id)
    if dp_eventos:
        membros_execucao = dp_eventos.membroexecucao_set.all()

    serializer = MembroExecucaoSerializer(membros_execucao, many=True)
    return render(request,'membrosExecucao/membros_execucao_table.html',{'membros_execucao':serializer.data})

@login_required(login_url='/auth-user/login-user')
def membroExecucaoForm(request):
    data = {}
    data['id_to_remove'] = int(request.GET.get('id')) 
    data['id_to_add'] = int(request.GET.get('id')) + 1
    data["prefix_id"] = 'collapse_endereco_input' if data['id_to_remove'] > 0 else 'collapse_endereco_input_0'
    data['hide_remove_button'] = "hide" if data["id_to_remove"] == 0 else "" 
    data['pessoas'] = Pessoas.objects.all()
    data['cidades'] = Cidade.objects.all()
    return render(request,'membrosExecucao/membro_execucao_form.html',data)

@login_required(login_url='/auth-user/login-user')
def membroExecucaoModal(request):
    id = request.GET.get('id')
    acao_id = request.GET.get('acao_id')
    evento_id = request.GET.get('evento_id')
    membro_execucao = None
    title = request.GET.get('title')

    data = {}
    data["state"] = "create_one"
    data["is_edit"] = False
    data['pessoas'] = Pessoas.objects.all()
    data['cidades'] = Cidade.objects.all()
    data['title'] = title

    if acao_id:
        data['acao'] = Acao.objects.get(id=acao_id)
    if evento_id:
        data['evento'] = DpEvento.objects.get(id=evento_id)
    if id:
        membro_execucao = MembroExecucao.objects.get(id=id)
        data["cidade_id"] = membro_execucao.cidade.id if membro_execucao.cidade else None
        data["pessoa_id"] = membro_execucao.pessoa.id
        data["is_edit"] = True
        data['membro_execucao'] = MembroExecucaoSerializer(membro_execucao).data 
    return render(request,'membrosExecucao/membro_execucao_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def membroExecucaoDemandasModal(request, membro_execucao_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/membroExecucao/'+membro_execucao_id, headers=headers)
    data = {}
    data["membro_execucao"] = json.loads(response.content.decode())
    return render(request,'membrosExecucao/membro_execucao_demandas_modal.html',data)

# @login_required(login_url='/auth-user/login-user')
# def alocacaoModalCadastrar(request):
#     id = request.GET.get('id')
#     alocacao = None
#     data = {}
#     if id:
#         alocacao = Alocacao.objects.get(id=id)
#         alocacao = AlocacaoSerializer(alocacao).data
#         data['alocacao'] = alocacao
#     return render(request,'alocacoes/modal_cadastrar_alocacao.html',data)

@login_required(login_url='/auth-user/login-user')
def saveMembroExecucao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/membroExecucao', json=body, headers=headers)
    return JsonResponse(json.loads(response.content.decode()),status=response.status_code, safe=False)

@login_required(login_url='/auth-user/login-user')
def editarMembroExecucao(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/membroExecucao/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarMembroExecucao(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/membroExecucao/'+str(codigo), headers=headers)
    
    return HttpResponse(status=response.status_code)


@login_required(login_url='/auth-user/login-user')
def membrosExecucaoSelect(request):
    data = {}
    if request.GET.get('membro_execucao_id'):
        data['membro_execucao_id'] = int(request.GET.get('membro_execucao_id'))
    acao_id = request.GET.get('acao_id')
    evento_id = request.GET.get('evento_id') if request.GET.get('evento_id') else request.GET.get('dp_evento_id')
    if evento_id:
        data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id=evento_id)
    else:
        data["membrosExecucao"] = MembroExecucao.objects.all()

    data["select_id"] = request.GET.get('select_id')
    data['title'] = request.GET.get('title')
    selectedId = request.GET.get('selected') if request.GET.get('selected') else request.GET.get('membro_execucao_id')
    selectedId = selectedId.strip() if selectedId else ""
    selectedId = int(selectedId) if selectedId else ""
    data["selected_membro_execucao_id"] = selectedId
    return render(request,'membrosExecucao/membroExecucaoSelect.html', data)


login_required(login_url='/auth-user/login-user')
def getMembrosExecucao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    params = {}
    if request.GET.get('evento_id'):
        params['evento_id'] = request.GET.get('evento_id')
    if request.GET.get('proposta_projeto_id'):
        params['proposta_projeto_id'] = request.GET.get('proposta_projeto_id')
    if request.GET.get('atividade_id'):
        atividade = Atividade.objects.get(id=request.GET.get('atividade_id'))
        params['proposta_projeto_id'] = atividade.proposta_projeto.id if atividade.proposta_projeto else None
    response = requests.get('http://localhost:8000/membroExecucao', params=params, headers=headers)
    pessoas = json.loads(response.content)
    return JsonResponse(pessoas,safe=False)

@login_required(login_url='/auth-user/login-user')
def getMembroExecucao(request, pk):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/membroExecucao/'+str(pk), headers=headers)
    return JsonResponse(json.loads(response.content),safe=False)