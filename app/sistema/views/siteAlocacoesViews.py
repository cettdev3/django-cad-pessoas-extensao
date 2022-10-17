from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.alocacaoSerializer import AlocacaoSerializer
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.alocacao import Alocacao
from sistema.models.curso import Curso
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth-user/login-user')
def alocacoesTable(request):
    print("dentro de alocacoes table")
    evento_id = request.GET.get('evento_id')
    print("eventoId: ", evento_id)
    alocacoes = Alocacao.objects
    if evento_id:
        alocacoes = alocacoes.filter(evento_id = evento_id)
    alocacoes = alocacoes.all()
    print(alocacoes)
    return render(request,'alocacoes/alocacoes_table.html',{'alocacoes':alocacoes})

@login_required(login_url='/auth-user/login-user')
def alocacaoModalCadastrar(request):
    id = request.GET.get('id')
    alocacao = None
    data = {}
    if id:
        alocacao = Alocacao.objects.get(id=id)
        alocacao = AlocacaoSerializer(alocacao).data
        data['alocacao'] = alocacao
        print(data)
    return render(request,'alocacoes/modal_cadastrar_alocacao.html',data)

# FIM PESSOAS