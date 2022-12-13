from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.pessoa import Pessoas
from sistema.models.cidade import Cidade
from sistema.models.acao import Acao
from django.contrib.auth.decorators import login_required
import requests
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
import json
from django.http import JsonResponse

@login_required(login_url='/auth-user/login-user')
def membrosExecucaoTable(request):
    acao_id = request.GET.get('acao_id')
    membros_execucao = MembroExecucao.objects
    if acao_id:
        membros_execucao = membros_execucao.filter(acao_id = acao_id)
    membros_execucao = membros_execucao.all()
    return render(request,'membrosExecucao/membros_execucao_table.html',{'membros_execucao':membros_execucao})

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
    membro_execucao = None
    data = {}
    data["state"] = "create_one"
    data["is_edit"] = False
    data['pessoas'] = Pessoas.objects.all()
    data['cidades'] = Cidade.objects.all()
    if acao_id:
        data['acao'] = Acao.objects.get(id=acao_id)
    if id:
        membro_execucao = MembroExecucao.objects.get(id=id)
        data["cidade_id"] = membro_execucao.cidade.id
        data["pessoa_id"] = membro_execucao.pessoa.id
        data["is_edit"] = True
        data['membro_execucao'] = MembroExecucaoSerializer(membro_execucao).data 
    return render(request,'membrosExecucao/membro_execucao_modal.html',data)

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
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    print("dentro da view do site",body)
    response = requests.put('http://localhost:8000/membroExecucao/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarMembroExecucao(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/membroExecucao/'+str(codigo), headers=headers)
    
    return HttpResponse(status=response.status_code)