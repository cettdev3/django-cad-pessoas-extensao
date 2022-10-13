from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.curso import Curso
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_pessoas(request):
    page_title = "Pessoas"
    count = 0
    pessoa = Pessoas.objects.all()
    print('-------------------------\n\n'+str(pessoa))
    for p in pessoa:
        count += 1

    return render(request,'pessoas/gerencia_pessoas.html',
    {'pessoas':pessoa,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def pessoasTable(request):
    nome = request.GET.get('nome')
    pessoas = Pessoas.objects
    if nome:
        pessoas = pessoas.filter(nome__contains = nome)
    pessoas = pessoas.all()
    return render(request,'pessoas/pessoas_table.html',{'pessoas':pessoas})

@login_required(login_url='/auth-user/login-user')
def visualizarPessoa(request,codigo):
    pessoa = Pessoas.objects.get(id=codigo)
    return render(request,'pessoas/visualizar_pessoas.html',{'pessoa':pessoa})

@login_required(login_url='/auth-user/login-user')
def pessoasModalCadastrar(request):
    id = request.GET.get('id')
    pessoa = None
    cursos = None
    data = {}
    if id:
        pessoa = Pessoas.objects.get(id=id)
        cursos = CursoSerializer(pessoa.cursos, many=True)
        print(cursos)
        if cursos:
            data['pessoa'] = pessoa
            data['cursos'] = cursos.data
    return render(request,'pessoas/modal_cadastrar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def cursosSelect(request):
    cursos = Curso.objects.all()
    return render(request,'pessoas/cursos_select.html',{'cursos':cursos})

@login_required(login_url='/auth-user/login-user')
def eliminarPessoa(request,codigo):
    user = Pessoas.objects.get(id=codigo)
    user.delete()
    return redirect('/gerenciar-pessoas')

# FIM PESSOAS