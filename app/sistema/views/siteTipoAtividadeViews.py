from django.shortcuts import render, redirect
from sistema.models.tipoAtividade import TipoAtividade
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

@login_required(login_url='/auth-user/login-user')
def gerenciarTipoAtividade(request):
    page_title = "Tipos de Atividades"
    count = 0
    tiposAtividades = TipoAtividade.objects.all()
    for p in tiposAtividades:
        count += 1

    return render(request,'tiposAtividades/tiposAtividadesGerenciar.html',
    {'tiposAtividades':tiposAtividades,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def tiposAtividadesTable(request):
    nome = request.GET.get('nome')
    tiposAtividades = TipoAtividade.objects
    if nome:
        tiposAtividades = tiposAtividades.filter(nome__contains = nome)
    tiposAtividades = tiposAtividades.all()
    return render(request,'tiposAtividades/tiposAtividadesTabela.html',{'tiposAtividades':tiposAtividades})

# @login_required(login_url='/auth-user/login-user')
# def visualizarTurno(request,codigo):
#     turno = Turno.objects.get(id=codigo)
#     return render(request,'turnos/visualizar_turno.html',{'turno':turno})

@login_required(login_url='/auth-user/login-user')
def tipoAtividadeModal(request):
    id = request.GET.get('id')
    tipoAtividade = None
    data = {}
    if id:
        tipoAtividade = TipoAtividade.objects.get(id=id)
        data['tipoAtividade'] = tipoAtividade
    return render(request,'tiposAtividades/tiposAtividadesModal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarTipoAtividade(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/tipos-atividades/'+str(codigo), headers=headers)
    return redirect('/gerenciarTipoAtividade')

@login_required(login_url='/auth-user/login-user')
def saveTipoAtividade(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/tipos-atividades', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarTipoAtividade(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/tipos-atividades/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def tipoAtividadeEditarModal(request, codigo):
    id = request.GET.get('id')
    tipoAtividade = TipoAtividade.objects.get(id=codigo)
    return render(request,'tiposAtividades/tiposAtividadesModal.html',{"tipoAtividade":tipoAtividade})

@login_required(login_url='/auth-user/login-user')
def tiposAtividadesSelect(request):
    data = {}
    if request.GET.get('tipo_atividade_id'):
        data['tipo_atividade_id'] = int(request.GET.get('tipo_atividade_id'))
    data["tiposAtividades"] = TipoAtividade.objects.all()
    data["select_id"] = request.GET.get('select_id')
    data["selected_tipo_atividade_id"] = int(request.GET.get('selected')) if request.GET.get('selected').strip() else None
    return render(request,'tiposAtividades/tiposAtividadesSelect.html', data)