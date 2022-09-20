from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.models import Pessoas
from django.contrib import messages
# Create your views here. teste

def menu_rapido(request):
    return render(request, 'home_menu.html')

def home(request):
    return render(request, 'base.html')

def gerencia_pessoas(request):
    count = 0
    pessoa = Pessoas.objects.all()
    print('-------------------------\n\n'+str(pessoa))
    for p in pessoa:
        count += 1

    return render(request,'gerencia_pessoas.html',{'pessoas':pessoa,'contagem':count})

def cadastrar_pessoas(request):
    return render(request,'cadastrar_pessoas.html')

def eliminarPessoa(request,codigo):
    user = Pessoas.objects.get(id=codigo)
    user.delete()
    return redirect('/gerenciar-pessoas')

def visualizarPessoa(request,codigo):
    user = Pessoas.objects.get(id=codigo)

    return render(request,'visualizar_pessoas.html',{'user':user})

def editarPessoa(request,codigo):
    user = Pessoas.objects.get(id=codigo)
    return render(request,'editar_pessoa.html',{'user':user})

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
    user.endereco = endereco
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
    qtd_contratacoes  = request.POST['qtd_contratacoes ']
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