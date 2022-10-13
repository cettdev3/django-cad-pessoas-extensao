from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.eventoSerializer import EventoSerializer
from sistema.models.curso import Curso
from sistema.models.endereco import Endereco
from sistema.models.cidade import Cidade
from sistema.models.evento import Evento
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_eventos(request):
    page_title = "eventos"
    count = 0
    eventos = Evento.objects.all()
    for p in eventos:
        count += 1

    return render(request,'eventos/gerencia_eventos.html',
    {'eventos':eventos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def eventosTable(request):
    nome = request.GET.get('nome')
    eventos = Evento.objects
    if nome:
        eventos = eventos.filter(nome__contains = nome)
    eventos = eventos.all()
    return render(request,'eventos/eventos_table.html',{'eventos':eventos})

@login_required(login_url='/auth-user/login-user')
def visualizarCurso(request,codigo):
    curso = Curso.objects.get(id=codigo)
    return render(request,'cursos/visualizar_curso.html',{'curso':curso})

@login_required(login_url='/auth-user/login-user')
def eventosModalCadastrar(request):
    id = request.GET.get('id')
    evento = None
    data = {}
    if id:
        evento = Evento.objects.get(id=id)
        data['evento'] = EventoSerializer(evento).data
        print(data)
    return render(request,'eventos/modal_cadastrar_evento.html',data)

@login_required(login_url='/auth-user/login-user')
def cidadesSelect(request):
    cidades = Cidade.objects.all()
    return render(request,'eventos/cidades_select.html',{'cidades':cidades})

@login_required(login_url='/auth-user/login-user')
def enderecosSelect(request):
    cidade_id = request.GET.get('cidade_id')
    print("cidade id: ",cidade_id)
    enderecos = Endereco.objects.filter(cidade_id=cidade_id).all()
    return render(request,'eventos/enderecos_select.html',{'enderecos':enderecos})

@login_required(login_url='/auth-user/login-user')
def eliminarEvento(request,codigo):
    print("dentro da rota")
    evento = Evento.objects.get(id=codigo)
    evento.delete()
    return redirect('/gerenciar-eventos')

# FIM PESSOAS