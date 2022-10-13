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
def menu_rapido(request):
    return render(request, 'home_menu.html')

@login_required(login_url='/auth-user/login-user')
def home(request):
    return render(request, 'base.html')

@login_required(login_url='/auth-user/login-user')
def cadastrar_pessoas(request):
    return render(request,'cadastrar_pessoas.html')

@login_required(login_url='/auth-user/login-user')
def editarPessoa(request,codigo):
    pessoa = Pessoas.objects.get(id=codigo)
    return render(request,'editar_pessoa.html',{'pessoa':pessoa})

@login_required(login_url='/auth-user/login-user')
def edicaoPessoa(request):
    id_ = request.POST['codigo']
    nome = request.POST['nome']
    email = request.POST['email']
    data_nascimento = request.POST['data_nascimento']
    telefone = request.POST['telefone']
    cpf = request.POST['cpf']
    rg = request.POST['rg']
    orgao_emissor = request.POST['orgao_emissor']
    endereco = request.POST['endereco']
    cep = request.POST['cep']
    cargo = request.POST['cargo']
    tipo = request.POST['tipo']
    banco = request.POST['banco']
    agencia = request.POST['agencia']
    conta = request.POST['conta']
    pix = request.POST['pix']
    qtd_contratacoes = request.POST['qtd_contratacoes']

    user = Pessoas.objects.get(id=id_)
    user.nome = nome
    user.email = email
    user.data_nascimento = data_nascimento
    user.telefone = telefone
    user.cpf = cpf
    user.rg = rg
    user.orgao_emissor = orgao_emissor
    user.cep = cep
    user.cargo = cargo
    user.tipo = tipo
    user.banco = banco
    user.agencia = agencia
    user.conta = conta
    user.pix =pix
    user.qtd_contratacoes = qtd_contratacoes
    user.save()

    messages.success(request,"Cadastro alterado com sucesso!")

    return redirect('/gerenciar-pessoas')

@login_required(login_url='/auth-user/login-user')
def registrar(request):
    nome = request.POST['nome']
    email = request.POST['email']
    data_nascimento = request.POST['data_nascimento']
    telefone = request.POST['telefone']
    cpf = request.POST['cpf']
    rg = request.POST['rg']
    orgao_emissor = request.POST['orgao_emissor']
    endereco = request.POST['endereco']
    cep = request.POST['cep']
    cargo = request.POST['cargo']
    tipo = request.POST['tipo']
    banco = request.POST['banco']
    agencia = request.POST['agencia']
    conta = request.POST['conta']
    pix = request.POST['pix']
    qtd_contratacoes  = request.POST['qtd_contratacoes']
    user_camunda = request.POST['user_camunda']
    

    cadastrar = Pessoas.objects.create(
        nome = nome,
        email = email,
        data_nascimento = data_nascimento,
        telefone = telefone,
        cpf = cpf,
        rg = rg,
        orgao_emissor = orgao_emissor,
        endereco = endereco,
        cep = cep,
        cargo = cargo,
        tipo = tipo,
        banco = banco,
        agencia = agencia,
        conta = conta,
        pix = pix,
        qtd_contratacoes = qtd_contratacoes,
        user_camunda = user_camunda

        )
    messages.success(request,'Cadastro realizado com sucesso!')
    return redirect('/gerenciar-pessoas')