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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from sistema.views.ticketApiViews import TicketApiView, TicketViewSets
from sistema.views.avaliacaoApiViews import AvaliacaoApiView, AvaliacaoDetailApiView
from sistema.views.enderecoApiViews import EnderecoApiView, EnderecoDetailApiView
from sistema.views.ensinoApiViews import EnsinoApiView, EnsinoDetailApiView
from sistema.views.membroExecucaoApiViews import MembroExecucaoApiView, MembroExecucaoDetailApiView
from sistema.views.pessoaApiViews import PessoaApiView, PessoaDetailApiView, PessoaViewSets
from sistema.views.galeriaApiViews import GaleriaApiView, GaleriaDetailApiView
from sistema.views.cidadeApiViews import CidadeApiView, CidadeDetailApiView
from sistema.views.acaoApiViews import AcaoApiView, AcaoDetailApiView
from sistema.views.escolaApiViews import EscolaApiView, EscolaDetailApiView
from sistema.views.alocacaoApiViews import AlocacaoApiView, AlocacaoDetailApiView
from sistema.views.cursoApiViews import CursoApiView, CursoDetailApiView
from sistema.views.servicoContratadoApiViews import ServicoContratadoApiView, ServicoContratadoDetailApiView
from sistema.views.turnoApiViews import TurnoApiView, TurnoDetailApiView
from sistema.views.departamentoApiViews import DepartamentoApiView, DepartamentoDetailApiView
from sistema.views.siteViews import home, cadastrar_pessoas, editarPessoa, edicaoPessoa, registrar
from sistema.views.sitePessoaViews import pessoasModalCadastrar, pessoasTable, pessoasSelect, cursosSelect, gerencia_pessoas, eliminarPessoa, visualizarPessoa, pessoasModalAlocar, savePessoa, editarPessoa
from sistema.views.siteCursoViews import gerencia_cursos, cursosTable, cursosModalCadastrar, eliminarCurso, editarCurso, saveCurso
from sistema.views.siteCidadeViews import gerencia_cidades, cidadesTable, cidadesModalCadastrar, eliminarCidade, saveCidade, editarCidade, cidadesSelect
from sistema.views.siteEnsinoViews import gerencia_ensinos, ensinosTable, ensinosModalCadastrar, eliminarEnsino, visualizarEnsino, saveEnsino, editarEnsino
from sistema.views.siteAlocacoesViews import alocacoesTable, alocacaoModalCadastrar, saveAlocacao, editarAlocacao, eliminarAlocacao, modalAlocar, horasTrabalhadas
from sistema.views.siteEnderecoViews import saveEndereco, editarEndereco, enderecosSelect
from sistema.views.siteEscolaViews import gerencia_escolas, escolasTable, escolasModalCadastrar, eliminarEscola, saveEscola, editarEscola, escolasSelect
from sistema.views.siteTestView import testeForm, testeModal, testeGerenciar, testeTabela, testeSave, testeEdit
from sistema.views.siteTurnoViews import gerencia_turnos, turnoTable, turnoModal, turnosSelect, saveTurno, eliminarTurno, editarTurno, turnosSelect
from sistema.views.siteAcaoViews import gerencia_acoes, acaoTable, acaoModal, acoesSelect, saveAcao, eliminarAcao, editarAcao, visualizarAcao
from sistema.views.siteDpEventoViews import gerencia_dp_eventos, dpEventoTable, dpEventoModal, dp_eventosSelect, saveDpEvento, eliminarDpEvento, editarDpEvento, relatorioDpEvento, visualizarDpEvento
from sistema.views.siteItinerarioItemViews import saveItinerarioItem, editarItinerarioItem, eliminarItinerarioItem
from sistema.views.siteComponentsView import calendario, filtrosRelatorioEventosModal, confirmDeleteModal, filterMultipleSelect
from sistema.views.siteMembroExecucaoViews import membrosExecucaoTable, membrosExecucaoDpEventoTable, membroExecucaoForm, membroExecucaoModal, saveMembroExecucao, editarMembroExecucao,eliminarMembroExecucao, membrosExecucaoSelect, membroExecucaoDemandasModal
from sistema.views.siteTicketViews import ticketModal, saveTicket, ticket_form, eliminarTicket, ticketModalEdit, editarTicket
from sistema.views.siteDepartamentoViews import gerencia_departamentos, departamentosTable, visualizarDepartamento, departamentosSelect, departamentosModalCadastrar, eliminarDepartamento, saveDepartamento, editarDepartamento
from sistema.views.siteItinerarioViews import saveItinerario, editarItinerario, eliminarItinerario
from sistema.views.siteTipoAtividadeViews import gerenciarTipoAtividade, tiposAtividadesTable, tipoAtividadeModal, saveTipoAtividade, eliminarTipoAtividade, tipoAtividadeEditarModal, editarTipoAtividade, tiposAtividadesSelect
from sistema.views.siteAtividadeViews import atividadesDpEventoTable, atividadesTable, atividadeModal, saveAtividade, eliminarAtividade, atividadeEditarModal, editarAtividade
from sistema.views.siteDataRemovidaViews import eliminarDataRemovida, createDataRemovida
from sistema.views.siteAvaliacaoViews import avaliacoesTable, eliminarAvaliacao, updateAvaliacao, avaliacaoModal, saveAvaliacao, avaliacoesDpEventoTable, avaliacaoRelatorio
from sistema.views.siteServicosContratadosViews import servicoContratadoModal, servicoContratadoTable, saveServicoContratado, deleteServicoContratado
from sistema.views.siteUserViews import usersSelect
from sistema.views.siteDemandaViews import gerencia_demandas, demandas_tabela
from sistema.views.siteServicoViews import ServicoModalCadastrar, eliminarServico, saveServico, editarServico
from sistema.views.siteGaleriaViews import (
    galeriaModal,
    galeriaTable,
    saveGaleria,
    deleteGaleria
)
from sistema.views.ticketApiViews import TicketApiView, TicketDetailApiView
from sistema.views.itinerarioApiViews import ItinerarioApiView, ItinerarioDetailApiView
from sistema.views.itinerarioItemApiViews import ItinerarioItemApiView, ItinerarioItemDetailApiView
from sistema.views.tipoAtividadeApiViews import TipoAtividadeApiView, TipoAtividadeDetailApiView
from sistema.views.atividadeApiViews import AtividadeApiView, AtividadeDetailApiView
from sistema.views.dataRemovidaApiViews import DataRemovidaApiView
from sistema.views.migrationsApiView import MigrationsViewSets
from sistema.views.dpEventoApiViews import DpEventoApiView, DpEventoDetailApiView
from sistema.views.servicoApiViews import ServicoApiView, ServicoDetailApiView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'auth-pessoas', PessoaViewSets, 'pessoas')
router.register(r'migrations', MigrationsViewSets, 'migration-acoes')
router.register(r'migrations', MigrationsViewSets, 'migrations-membros-execucao')
router.register(r'migrations', MigrationsViewSets, 'migrate-tickets')
router.register(r'tickets', TicketViewSets, 'complete-prestacao-contas')

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),

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
    path("pessoasSelect",pessoasSelect),
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
    
    # ROTAS PARA USERS
    path("usersSelect",usersSelect),
    
    # ROTAS PARA DEPARTAMENTOS
    path("gerenciar-departamentos",gerencia_departamentos),
    path("departamentosTable",departamentosTable),
    path("departamentosModalCadastrar",departamentosModalCadastrar),
    path("departamentosSelect",departamentosSelect),
    path("eliminarDepartamento/<codigo>",eliminarDepartamento),
    path("saveDepartamento",saveDepartamento),
    path("editarDepartamento/<codigo>",editarDepartamento),
    path("visualizarDepartamento/<codigo>",visualizarDepartamento),

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
    path("escolasSelect",escolasSelect),
    
    # ROTAS PARA DEMANDAS
    path("gerencia_demandas",gerencia_demandas),
    path("demandas_tabela",demandas_tabela),
    
    # ROTAS PARA ALOCAÇÔES
    path("alocacoesTable",alocacoesTable),
    path("horasTrabalhadas",horasTrabalhadas),
    path("modalAlocar",modalAlocar),
    path("alocacaoModalCadastrar",alocacaoModalCadastrar),
    path("saveAlocacao",saveAlocacao),
    path("editarAlocacao/<codigo>",editarAlocacao),
    path("eliminarAlocacao/<codigo>",eliminarAlocacao),
    
    # ROTAS PARA ENSINO
    path("gerenciar-ensinos",gerencia_ensinos),
    path("ensinosTable",ensinosTable),
    path("ensinosModalCadastrar",ensinosModalCadastrar),
    path("eliminarEnsino/<codigo>",eliminarEnsino),
    path("visualizarEnsino/<codigo>",visualizarEnsino),
    path("saveEnsino",saveEnsino),
    path("editarEnsino/<codigo>",editarEnsino),
    
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
    
    # ROTAS PARA DATAS REMOVIDAS
    path("createDataRemovida",createDataRemovida),
    path("eliminarDataRemovida/<codigo>",eliminarDataRemovida),
   
    # ROTAS PARA TIPOS DE ATIVIDADES
    path("gerenciarTipoAtividade", gerenciarTipoAtividade),
    path("tiposAtividadesTable", tiposAtividadesTable),
    path("tipoAtividadeModal", tipoAtividadeModal),
    path("saveTipoAtividade", saveTipoAtividade),
    path("tiposAtividadesSelect", tiposAtividadesSelect),
    path("eliminarTipoAtividade/<codigo>", eliminarTipoAtividade),
    path("tipoAtividadeEditarModal/<codigo>", tipoAtividadeEditarModal),
    path("editarTipoAtividade/<codigo>", editarTipoAtividade),
   
    # ROTAS PARA ATIVIDADES
    path("atividadesTable", atividadesTable),
    path("atividadeModal", atividadeModal),
    path("saveAtividade", saveAtividade),
    path("eliminarAtividade/<codigo>", eliminarAtividade),
    path("atividadeEditarModal/<codigo>", atividadeEditarModal),
    path("editarAtividade/<codigo>", editarAtividade),
    path("atividadesDpEventoTable", atividadesDpEventoTable),
    
    # ROTAS PARA MEMBROS DE EXECUCAO
    path("membrosExecucaoTable",membrosExecucaoTable),
    path("membrosExecucaoDpEventoTable",membrosExecucaoDpEventoTable),
    path("membroExecucaoForm",membroExecucaoForm),
    path("membroExecucaoModal",membroExecucaoModal),
    path("saveMembroExecucao",saveMembroExecucao),
    path("membrosExecucaoSelect",membrosExecucaoSelect),
    path("editarMembroExecucao/<codigo>",editarMembroExecucao),
    path("eliminarMembroExecucao/<codigo>",eliminarMembroExecucao),
    path("membroExecucaoDemandasModal/<membro_execucao_id>",membroExecucaoDemandasModal),

    # ROTAS PARA ACOES
    path("gerencia_acoes",gerencia_acoes),
    path("acaoTable",acaoTable),
    path("acaoModal",acaoModal),
    path("acoesSelect",acoesSelect),
    path("saveAcao",saveAcao),
    path("editarAcao/<codigo>",editarAcao),
    path("eliminarAcao/<codigo>",eliminarAcao),
    path("acoesSelect",acoesSelect),
    path("visualizarAcao/<codigo>",visualizarAcao),

    # ROTAS PARA EVENTOS
    path("gerencia_dp_eventos", gerencia_dp_eventos), 
    path("dpEventoTable", dpEventoTable), 
    path("dpEventoModal", dpEventoModal), 
    path("dp_eventosSelect", dp_eventosSelect), 
    path("saveDpEvento", saveDpEvento), 
    path("eliminarDpEvento/<codigo>", eliminarDpEvento), 
    path("editarDpEvento/<codigo>", editarDpEvento), 
    path("acoesSelect", acoesSelect),
    path("visualizarDpEvento/<codigo>", visualizarDpEvento),
    path("relatorioDpEvento", relatorioDpEvento),
   
    # ROTAS PARA TICKETS
    path("ticketModal",ticketModal),
    path("ticketModalEdit/<ticket_id>",ticketModalEdit),
    path("saveTicket",saveTicket),
    path("editarTicket/<ticket_id>",editarTicket),
    path("ticket_form",ticket_form),
    path("eliminarTicket/<ticket_id>",eliminarTicket),
    
    # ROTAS PARA SERVICOS
    path("ServicoModalCadastrar",ServicoModalCadastrar),
    path("editarServico/<codigo>",editarServico),
    path("eliminarServico/<codigo>",eliminarServico),
    path("saveServico",saveServico),

    # ROTAS PARA AVALIACOES
    path("avaliacoesDpEventoTable",avaliacoesDpEventoTable),
    path("avaliacaoModal",avaliacaoModal),
    path("avaliacoesTable",avaliacoesTable), 
    path("updateAvaliacao/<id>",updateAvaliacao), 
    path("eliminarAvaliacao/<id>",eliminarAvaliacao), 
    path("saveAvaliacao",saveAvaliacao), 
    path("avaliacaoRelatorio/<id>",avaliacaoRelatorio),
    
    # ROTAS PARA ITENS DE ITINERARIO
    path("saveItinerarioItem",saveItinerarioItem),
    path("editarItinerarioItem/<codigo>",editarItinerarioItem),
    path("eliminarItinerarioItem/<codigo>",eliminarItinerarioItem),
    
    # ROTAS PARA ITINERARIOS
    path("saveItinerario", saveItinerario), 
    path("editarItinerario/<codigo>", editarItinerario), 
    path("eliminarItinerario/<codigo>", eliminarItinerario),
        
    # ROTAS PARA COMPONENTES
    path("calendario",calendario),
    path("filtrosRelatorioEventosModal",filtrosRelatorioEventosModal),
    path("confirmDeleteModal",confirmDeleteModal),
    path("filterMultipleSelect", filterMultipleSelect),

    # ROTAS PARA SERVICOS CONTRATADOS
    path("servicoContratadoModal",servicoContratadoModal),
    path("servicoContratadoTable",servicoContratadoTable),
    path("saveServicoContratado",saveServicoContratado),
    path("deleteServicoContratado/<servico_contratado_id>",deleteServicoContratado),

    # ROTAS PARA GALERIAS
    path("galeriaModal", galeriaModal),
    path("galeriaTable", galeriaTable),
    path("saveGaleria", saveGaleria),
    path("deleteGaleri", deleteGaleria),

    # ROTAS DE API
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path("pessoas", PessoaApiView.as_view()),
    path("pessoas/<int:pessoa_id>", PessoaDetailApiView.as_view()),

    path("galerias", GaleriaApiView.as_view()),
    path("galerias/<int:galeria_id>", GaleriaDetailApiView.as_view()),
    
    path("enderecos", EnderecoApiView.as_view()),
    path('enderecos/<int:endereco_id>', EnderecoDetailApiView.as_view()),
    
    path("ensino", EnsinoApiView.as_view()),
    path('ensino/<int:ensino_id>', EnsinoDetailApiView.as_view()),

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
    
    path("acoes", AcaoApiView.as_view()),
    path('acoes/<int:acao_id>', AcaoDetailApiView.as_view()),
   
    path("membroExecucao", MembroExecucaoApiView.as_view()),
    path('membroExecucao/<int:membro_execucao_id>', MembroExecucaoDetailApiView.as_view()),
    
    path("tickets", TicketApiView.as_view()),
    path('tickets/<int:ticket_id>', TicketDetailApiView.as_view()),
    
    path("itinerarios", ItinerarioApiView.as_view()),
    path('itinerarios/<int:itinerario_id>', ItinerarioDetailApiView.as_view()),
    
    path("itinerario-itens", ItinerarioItemApiView.as_view()),
    path('itinerario-itens/<int:itinerario_item_id>', ItinerarioItemDetailApiView.as_view()),
    
    path("tipos-atividades", TipoAtividadeApiView.as_view()),
    path('tipos-atividades/<int:tipo_atividade_id>', TipoAtividadeDetailApiView.as_view()),
    
    path("atividades", AtividadeApiView.as_view()),
    path('atividades/<int:atividade_id>', AtividadeDetailApiView.as_view()),
    
    path("dp-eventos", DpEventoApiView.as_view()),
    path('dp-eventos/<int:dp_evento_id>', DpEventoDetailApiView.as_view()),
   
    path("departamentos", DepartamentoApiView.as_view()),
    path('departamentos/<int:departamento_id>', DepartamentoDetailApiView.as_view()),
    
    path("servicos", ServicoApiView.as_view()),
    path('servicos/<int:servico_id>', ServicoDetailApiView.as_view()),
    
    path("datas-removidas", DataRemovidaApiView.as_view()),

    path("servicos-contratados", ServicoContratadoApiView.as_view()),
    path('servicos-contratados/<int:servico_contratado_id>', ServicoContratadoDetailApiView.as_view()),

    # ROTAS DE AUTENTICAÇÂO
    path("auth-user/", include('django.contrib.auth.urls')),
    path("auth-user/", include('authentication.urls')),

    path('', include(router.urls)),
]
