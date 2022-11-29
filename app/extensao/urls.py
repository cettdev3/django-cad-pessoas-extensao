"""extensao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from sistema.views.ticketApiViews import TicketApiView
from sistema.views.avaliacaoApiViews import AvaliacaoApiView, AvaliacaoDetailApiView
from sistema.views.enderecoApiViews import EnderecoApiView, EnderecoDetailApiView
from sistema.views.eventoApiViews import EventoApiView, EventoDetailApiView
from sistema.views.pessoaApiViews import PessoaApiView, PessoaDetailApiView
from sistema.views.cidadeApiViews import CidadeApiView, CidadeDetailApiView
from sistema.views.escolaApiViews import EscolaApiView, EscolaDetailApiView
from sistema.views.alocacaoApiViews import AlocacaoApiView, AlocacaoDetailApiView
from sistema.views.cursoApiViews import CursoApiView, CursoDetailApiView
from sistema.views.turnoApiViews import TurnoApiView, TurnoDetailApiView
from sistema.views.siteViews import home, cadastrar_pessoas, editarPessoa, edicaoPessoa, registrar
from sistema.views.sitePessoaViews import pessoasModalCadastrar, pessoasTable, cursosSelect, gerencia_pessoas, eliminarPessoa, visualizarPessoa, pessoasModalAlocar, savePessoa, editarPessoa
from sistema.views.siteCursoViews import gerencia_cursos, cursosTable, cursosModalCadastrar, eliminarCurso, editarCurso, saveCurso
from sistema.views.siteCidadeViews import gerencia_cidades, cidadesTable, cidadesModalCadastrar, eliminarCidade, saveCidade, editarCidade, cidadesSelect
from sistema.views.siteEventoViews import gerencia_eventos, eventosTable, eventosModalCadastrar, eliminarEvento, visualizarEvento, saveEvento, editarEvento
from sistema.views.siteAlocacoesViews import alocacoesTable, alocacaoModalCadastrar, saveAlocacao, editarAlocacao, eliminarAlocacao, modalAlocar 
from sistema.views.siteEnderecoViews import saveEndereco, editarEndereco, enderecosSelect
from sistema.views.siteEscolaViews import gerencia_escolas, escolasTable, escolasModalCadastrar, eliminarEscola, saveEscola, editarEscola
from sistema.views.siteTestView import testeForm, testeModal, testeGerenciar, testeTabela, testeSave, testeEdit
from sistema.views.siteTurnoViews import gerencia_turnos, turnoTable, turnoModal, turnosSelect, saveTurno, eliminarTurno, editarTurno, turnosSelect

urlpatterns = [
    # ROTAS DO SITE
    path('admin/', admin.site.urls),
    path("eliminarPessoa/<codigo>", eliminarPessoa),
    path("visualizarPessoa/<codigo>", visualizarPessoa),
    path("editarPessoa/<codigo>", editarPessoa),
    path("edicaoPessoa",edicaoPessoa),
    path("registrar",registrar),

    # ROTAS PARA PESSOAS
    path("",gerencia_pessoas),
    path("home",gerencia_pessoas),
    path("gerenciar-pessoas",gerencia_pessoas),
    path("pessoasTable",pessoasTable),
    path("pessoasModalCadastrar",pessoasModalCadastrar),
    path("pessoasModalAlocar",pessoasModalAlocar),
    path("cursosSelect", cursosSelect),
    path("cadastrar-pessoas",cadastrar_pessoas),
    path("savePessoa", savePessoa),
    path("editarPessoa/<codigo>", editarPessoa),
    
    # ROTAS PARA CURSOS
    path("gerenciar-cursos",gerencia_cursos),
    path("cursosTable",cursosTable),
    path("cursosModalCadastrar",cursosModalCadastrar),
    path("eliminarCurso/<codigo>",eliminarCurso),
    path("saveCurso",saveCurso),
    path("editarCurso/<codigo>",editarCurso),
    
    # ROTAS PARA ENDERECOS
    path("saveEndereco",saveEndereco),
    path("editarEndereco/<codigo>",editarEndereco),
    path("enderecosSelect",enderecosSelect),
   
    # ROTAS PARA CIDADES
    path("gerenciar-cidades",gerencia_cidades),
    path("cidadesTable",cidadesTable),
    path("cidadesModalCadastrar",cidadesModalCadastrar),
    path("eliminarCidade/<codigo>",eliminarCidade),
    path("saveCidade",saveCidade),
    path("editarCidade/<codigo>",editarCidade),
    path("cidadesSelect",cidadesSelect),
    
    # ROTAS PARA ESCOLAS
    path("gerenciar-escolas",gerencia_escolas),
    path("escolasTable",escolasTable),
    path("escolasModalCadastrar",escolasModalCadastrar),
    path("eliminarEscola/<codigo>",eliminarEscola),
    path("saveEscola",saveEscola),
    path("editarEscola/<escola_id>",editarEscola),
    
    # ROTAS PARA ALOCAÇÔES
    path("alocacoesTable",alocacoesTable),
    path("modalAlocar",modalAlocar),
    path("alocacaoModalCadastrar",alocacaoModalCadastrar),
    path("saveAlocacao",saveAlocacao),
    path("editarAlocacao/<codigo>",editarAlocacao),
    path("eliminarAlocacao/<codigo>",eliminarAlocacao),
    
    # ROTAS PARA EVENTOS
    path("gerenciar-eventos",gerencia_eventos),
    path("eventosTable",eventosTable),
    path("eventosModalCadastrar",eventosModalCadastrar),
    path("eliminarEvento/<codigo>",eliminarEvento),
    path("visualizarEvento/<codigo>",visualizarEvento),
    path("saveEvento",saveEvento),
    path("editarEvento/<codigo>",editarEvento),
    
    # ROTAS PARA TESTES
    path("testeForm",testeForm),
    path("testeSave",testeSave),
    path("testeEdit",testeEdit),
    path("testeForm",testeForm),
    path("testeModal",testeModal),
    path("testeGerenciar",testeGerenciar),
    path("testeTabela",testeTabela),
   
    # ROTAS PARA TURNOS
    path("gerencia_turnos",gerencia_turnos),
    path("turnoTable",turnoTable),
    path("turnoModal",turnoModal),
    path("turnosSelect",turnosSelect),
    path("saveTurno",saveTurno),
    path("editarTurno/<codigo>",editarTurno),
    path("eliminarTurno/<codigo>",eliminarTurno),
    path("turnosSelect",turnosSelect),

    # ROTAS DE API
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path("pessoas", PessoaApiView.as_view()),
    path("pessoas/<int:pessoa_id>", PessoaDetailApiView.as_view()),
    
    path("enderecos", EnderecoApiView.as_view()),
    path('enderecos/<int:endereco_id>', EnderecoDetailApiView.as_view()),
    
    path("eventos", EventoApiView.as_view()),
    path('eventos/<int:evento_id>', EventoDetailApiView.as_view()),

    path("cidades", CidadeApiView.as_view()),
    path('cidades/<int:cidade_id>', CidadeDetailApiView.as_view()),

    path("avaliacoes", AvaliacaoApiView.as_view()),
    path('avaliacoes/<int:avaliacao_id>', AvaliacaoDetailApiView.as_view()),
    
    path("alocacoes", AlocacaoApiView.as_view()),
    path('alocacoes/<int:alocacao_id>', AlocacaoDetailApiView.as_view()),
    
    path("cursos", CursoApiView.as_view()),
    path('cursos/<int:curso_id>', CursoDetailApiView.as_view()),
    
    path("escolas", EscolaApiView.as_view()),
    path('escolas/<int:escola_id>', EscolaDetailApiView.as_view()),
    
    path("turnos", TurnoApiView.as_view()),
    path('turnos/<int:turno_id>', TurnoDetailApiView.as_view()),
    
    path("tickets", TicketApiView.as_view()),

    # ROTAS DE AUTENTICAÇÂO
    path("auth-user/", include('django.contrib.auth.urls')),
    path("auth-user/", include('authentication.urls'))
]
