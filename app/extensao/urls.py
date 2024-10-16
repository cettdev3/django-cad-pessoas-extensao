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
from sistema.views.ticketApiViews import TicketApiView
from sistema.views.avaliacaoApiViews import AvaliacaoApiView, AvaliacaoDetailApiView
from sistema.views.enderecoApiViews import EnderecoApiView, EnderecoDetailApiView
from sistema.views.ensinoApiViews import EnsinoApiView, EnsinoDetailApiView
from sistema.views.membroExecucaoApiViews import MembroExecucaoApiView, MembroExecucaoDetailApiView
from sistema.views.pessoaApiViews import PessoaApiView, PessoaDetailApiView, PessoaViewSets
from sistema.views.galeriaApiViews import GaleriaApiView, GaleriaDetailApiView
from sistema.views.imagemApiViews import ImagemApiView, ImagemDetailApiView
from sistema.views.cidadeApiViews import CidadeApiView, CidadeDetailApiView
from sistema.views.acaoApiViews import AcaoApiView, AcaoDetailApiView
from sistema.views.escolaApiViews import EscolaApiView, EscolaDetailApiView
from sistema.views.alocacaoApiViews import AlocacaoApiView, AlocacaoDetailApiView
from sistema.views.cursoApiViews import CursoApiView, CursoDetailApiView
from sistema.views.servicoContratadoApiViews import ServicoContratadoApiView, ServicoContratadoDetailApiView
from sistema.views.turnoApiViews import TurnoApiView, TurnoDetailApiView
from sistema.views.departamentoApiViews import DepartamentoApiView, DepartamentoDetailApiView
from sistema.views.siteViews import home, cadastrar_pessoas, editarPessoa, edicaoPessoa, registrar
from sistema.views.sitePessoaViews import getPessoas, pessoasModalCadastrar, pessoasTable, pessoasSelect, cursosSelect, gerencia_pessoas, eliminarPessoa, visualizarPessoa, pessoasModalAlocar, savePessoa, editarPessoa
from sistema.views.siteCursoViews import gerencia_cursos, cursosTable, cursosModalCadastrar, eliminarCurso, editarCurso, saveCurso
from sistema.views.siteCidadeViews import getCidades, gerencia_cidades, cidadesTable, cidadesModalCadastrar, eliminarCidade, saveCidade, editarCidade, cidadesSelect, cidadeForm
from sistema.views.siteEnsinoViews import gerencia_ensinos, ensinosTable, ensinosModalCadastrar, eliminarEnsino, visualizarEnsino, saveEnsino, editarEnsino, getEnsino, createEventoFromEnsino
from sistema.views.siteAlocacoesViews import formAlocacaoMembroEquipe, alocacoesTable, alocacaoModalCadastrar, saveAlocacao, editarAlocacao, eliminarAlocacao, modalAlocar, horasTrabalhadas
from sistema.views.siteEnderecoViews import saveEndereco, editarEndereco, enderecosSelect
from sistema.views.siteEscolaViews import gerencia_escolas, escolasTable, escolasModalCadastrar, eliminarEscola, saveEscola, editarEscola, escolasSelect
from sistema.views.siteTestView import testeForm, testeModal, testeGerenciar, testeTabela, testeSave, testeEdit
from sistema.views.siteTurnoViews import gerencia_turnos, turnoTable, turnoModal, turnosSelect, saveTurno, eliminarTurno, editarTurno, turnosSelect
from sistema.views.siteAcaoViews import gerencia_acoes, acaoTable, acaoModal, acoesSelect, saveAcao, eliminarAcao, editarAcao, visualizarAcao
from sistema.views.siteDpEventoViews import gerencia_dp_eventos, dpEventoTable, dpEventoModal, dp_eventosSelect, saveDpEvento, eliminarDpEvento, editarDpEvento, relatorioDpEvento, visualizarDpEvento, relatorioSintetico, relatorioPorEvento
from sistema.views.siteItinerarioItemViews import saveItinerarioItem, editarItinerarioItem, eliminarItinerarioItem
from sistema.views.siteComponentsView import calendario, filtrosRelatorioEventosModal, confirmDeleteModal, filterMultipleSelect
from sistema.views.siteMembroExecucaoViews import getMembroExecucao, getMembrosExecucao, membrosExecucaoTable, membrosExecucaoDpEventoTable, membroExecucaoForm, membroExecucaoModal, saveMembroExecucao, editarMembroExecucao,eliminarMembroExecucao, membrosExecucaoSelect, membroExecucaoDemandasModal
from sistema.views.siteTicketViews import ticketModal, saveTicket, ticket_form, ticket_form_collapsable, eliminarTicket, ticketModalEdit,updateTicket, editarTicket
from sistema.views.siteDepartamentoViews import gerencia_departamentos, departamentosTable, visualizarDepartamento, departamentosSelect, departamentosModalCadastrar, eliminarDepartamento, saveDepartamento, editarDepartamento
from sistema.views.siteItinerarioViews import saveItinerario, editarItinerario, eliminarItinerario
from sistema.views.siteTipoAtividadeViews import gerenciarTipoAtividade, tiposAtividadesTable, tipoAtividadeModal, saveTipoAtividade, eliminarTipoAtividade, tipoAtividadeEditarModal, editarTipoAtividade, tiposAtividadesSelect
from sistema.views.siteAtividadeViews import atividadesDpEventoTable, atividadesTable, atividadeModal, saveAtividade, deleteAtividade, getAtividadeDrawer, editarAtividade, atividadeSelect, atividadeForm, getAtividade
from sistema.views.siteDataRemovidaViews import eliminarDataRemovida, createDataRemovida
from sistema.views.siteAvaliacaoViews import avaliacoesTable, eliminarAvaliacao, updateAvaliacao, avaliacaoModal, saveAvaliacao, avaliacoesDpEventoTable, avaliacaoRelatorio
from sistema.views.siteServicosContratadosViews import servicoContratadoModal, servicoContratadoTable, saveServicoContratado, deleteServicoContratado
from sistema.views.siteUserViews import usersSelect
from sistema.views.siteDemandaViews import gerencia_demandas, demandas_tabela, relatorio_sintetico, importDemandaModal, saveBatchDemanda, demandasSelect
from sistema.views.siteServicoViews import ServicoModalCadastrar, eliminarServico, saveServico, editarServico
from sistema.views.siteMembroExecucaoRoles import getMembroExecucaoRoles, getMembroExecucaoRoleForm, membroExecucaoRoleCreate
from sistema.views.cotecViews.projetosCotecViews import (
    projetoCotecForm, 
    projetoCotecIndex, 
    orcamentoTable,
    proposta_projeto_view,
    menuStatusProposta,
    pessoaModal, 
    pessoaCreate, 
    selectMultipleComponent, 
    membroEquipeForm,
    getMultipleFormComponent,
    createPropostaProjeto, 
    propostasTable, 
    updateAtividade, 
    createAtividade, 
    removeAtividade, 
    updateMembroEquipe, 
    createMembroEquipe, 
    removeMembroEquipe,
    updateItemOrcamento, 
    createItemOrcamento, 
    removeItemOrcamento,
    projetoCotecSuccess,
    updatePropostaProjeto,
    removePropostaProjeto,
    showPropostaProjeto,
    createProjetoFromProposta,
    itemOrcamentoForm
)

from sistema.views.siteGaleriaViews import (
    galeriaModal,
    galeriaTable,
    saveGaleria,
    deleteGaleria
)
from sistema.views.siteAtividadeSectionViews import (
    atividadeSectionModal,
    atividadeSectionTable,
    saveAtividadeSection,
    deleteAtividadeSection,
    updateAtividadeSection,
    atividadeSectionComponent,
)

from sistema.views.siteImagemViews import (
    deleteImagem,
    saveImagem
)

from sistema.views.siteAnexoViews import (
    deleteAnexo,
    saveAnexo
)


from sistema.views.siteComentarioViews import (
    # updateComentario, 
    createComentario, 
    # removeComentario
)

from sistema.views.siteRecursoViews import (
    recursoForm,
    recursoSave,
    recursoEdit,
    recursoTabela,
    recursoDelete,
)

from sistema.views.siteRelatorioViews import (
    relatorioHorasTrabalhadasProfessores
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
from sistema.views.atividadeSectionApiViews import AtividadeSectionApiView, AtividadeSectionDetailApiView
from sistema.views.anexoApiViews import AnexoApiView, AnexoDetailApiView
from sistema.views.comentarioApiViews import ComentarioApiView, ComentarioDetailApiView
from sistema.views.emailApiViews import EmailApiView
from sistema.views.membroExecucaoRoleApiViews import MembroExecucaoRoleApiView, MembroExecucaoRoleDetailApiView
from sistema.views.recursoApiView import RecursoApiView, RecursoDetailApiView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'auth-pessoas', PessoaViewSets, 'pessoas')

# as rotas da migration controller servem para migrar os dados do banco de dados antigo para o novo
# a ordem da migrações deve ser a mesma ordem que as rotas estão declaradas
# so devem ser usadas uma unica vez no momento do deploy da nova feature
# router.register(r'migrations', MigrationsViewSets, 'migration-acoes')
# router.register(r'migrations', MigrationsViewSets, 'migrations-membros-execucao')
# router.register(r'migrations', MigrationsViewSets, 'migrate-tickets')
# router.register(r'migrations', MigrationsViewSets, 'seed-atividades-galeria')
# router.register(r'migrations', MigrationsViewSets, 'transferir-evento-escola')
# router.register(r'migrations', MigrationsViewSets, 'create-secao-atividades')
# router.register(r'migrations', MigrationsViewSets, 'update-beneficiario-tickets')
# router.register(r'migrations', MigrationsViewSets, 'update-atividades-extensao')
# router.register(r'migrations', MigrationsViewSets, 'create-atividade-categorias')
# router.register(r'migrations', MigrationsViewSets, 'set-atividade-categorias')
# router.register(r'migrations', MigrationsViewSets, 'create-cidades')

# router.register(r'tickets', TicketViewSets, 'complete-prestacao-contas')

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

    
    # ROTAS DO COTEC
    path("cotec-projeto-index", projetoCotecIndex, name="cotec-projeto-index"),
    path("cotec-projeto-success", projetoCotecSuccess, name="cotec-projeto-success"),
    path("cotec-projeto-form", projetoCotecForm, name="cotec-projeto-form"),
    path("pessoa-modal", pessoaModal, name="pessoa-modal"),
    path("pessoa-create", pessoaCreate, name="pessoa-create"),
    path("select-multiple-component", selectMultipleComponent, name="select-multiple-component"),
    path("membro-equipe-form", membroEquipeForm, name="membro-equipe-form"),
    path("multiple-form-component", getMultipleFormComponent, name="multiple-form-component"),
    path("create-proposta-projeto", createPropostaProjeto, name="create-proposta-projeto"),
    path("update-proposta-projeto/<pk>", updatePropostaProjeto, name="update-proposta-projeto"),
    path("remove-proposta-projeto/<pk>", removePropostaProjeto, name="remove-proposta-projeto"),
    path("create-projeto-proposta/<pk>", createProjetoFromProposta, name="create-projeto-proposta"),
    path("show-proposta-projeto/<pk>", showPropostaProjeto, name="show-proposta-projeto"),
    path("proposta-projeto-table", propostasTable, name="proposta-projeto-table"),
    path("update-atividade/<pk>", updateAtividade, name="update-atividade"),
    path("create-atividade", createAtividade, name="create-atividade"),
    path("remove-atividade/<pk>", removeAtividade, name="remove-atividade"),
    path("update-membro-equipe/<pk>", updateMembroEquipe, name="update-membro-equipe"),
    path("create-membro-equipe", createMembroEquipe, name="create-membro-equipe"),
    path("remove-membro-equipe/<pk>", removeMembroEquipe, name="remove-membro-equipe"),
    path("update-item-orcamento/<pk>", updateItemOrcamento, name="update-item-orcamento"),
    path("create-item-orcamento", createItemOrcamento, name="create-item-orcamento"),
    path("remove-item-orcamento/<pk>", removeItemOrcamento, name="remove-item-orcamento"),
    path("item-orcamento-form", itemOrcamentoForm, name="item-orcamento-form"),
    path("orcamento-table", orcamentoTable, name="orcamento-table"),
    path("proposta-projeto-view/<pk>", proposta_projeto_view, name="proposta-projeto-view"),
    path("status-proposta-menu", menuStatusProposta, name="status-proposta-menu"),

    # ROTAS PARA COMENTARIOS
    # path("update-comentario/<pk>", updateComentario, name="update-comentario"),
    path("create-comentario", createComentario, name="create-comentario"),
    # path("remove-comentario/<pk>", removeComentario, name="remove-comentario"),

    # RELATORIOS
    path("relatorioHorasTrabalhadasProfessores", relatorioHorasTrabalhadasProfessores, name="relatorio-horas-trabalhadas"),

    # ROTAS PARA PESSOAS
    path("",gerencia_dp_eventos),
    path("home",gerencia_dp_eventos, name="home"),
    path("gerenciar-pessoas",gerencia_pessoas),
    path("pessoasTable",pessoasTable),
    path("pessoasSelect",pessoasSelect),
    path("pessoasModalCadastrar",pessoasModalCadastrar),
    path("getPessoas",getPessoas),
    path("pessoasModalAlocar",pessoasModalAlocar),
    path("cursosSelect", cursosSelect, name="cursos-select"),
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
    path("getCidades",getCidades),
    path("cidadesModalCadastrar",cidadesModalCadastrar),
    path("eliminarCidade/<codigo>",eliminarCidade),
    path("saveCidade",saveCidade),
    path("editarCidade/<codigo>",editarCidade),
    path("cidadesSelect",cidadesSelect),
    path("cidadeForm",cidadeForm),
    
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
    path("relatorio_sintetico",relatorio_sintetico),
    path("importDemandaModal",importDemandaModal),
    path("saveBatchDemanda",saveBatchDemanda),
    path("saveBatchDemanda",saveBatchDemanda),
    path("demandasSelect",demandasSelect),
    
    # ROTAS PARA ALOCAÇÔES
    path("alocacoesTable",alocacoesTable),
    path("formAlocacaoMembroEquipe",formAlocacaoMembroEquipe, name="form-alocacao-membro-equipe"),
    path("horasTrabalhadas",horasTrabalhadas),
    path("modalAlocar",modalAlocar),
    path("alocacaoModalCadastrar",alocacaoModalCadastrar),
    path("saveAlocacao",saveAlocacao, name="save-alocacao"),
    path("editarAlocacao/<codigo>",editarAlocacao, name="editar-alocacao"),
    path("eliminarAlocacao/<codigo>",eliminarAlocacao, name= "eliminar-alocacao"),
    
    # ROTAS PARA ENSINO
    path("gerenciar-ensinos",gerencia_ensinos),
    path("ensinosTable",ensinosTable),
    path("ensinosModalCadastrar",ensinosModalCadastrar),
    path("eliminarEnsino/<codigo>",eliminarEnsino),
    path("visualizarEnsino/<codigo>",visualizarEnsino),
    path("saveEnsino",saveEnsino),
    path("editarEnsino/<codigo>",editarEnsino),
    path("getEnsino/<ensino_id>",getEnsino),
    path("createEventoFromEnsino/<ensino_id>",createEventoFromEnsino),
    
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
    path("deleteAtividade/<atividade_id>", deleteAtividade),
    path("getAtividadeDrawer/<atividade_id>", getAtividadeDrawer),
    path("editarAtividade/<atividade_id>", editarAtividade),
    path("atividadesDpEventoTable", atividadesDpEventoTable),
    path("atividadeSelect", atividadeSelect),
    path("atividadeForm", atividadeForm),
    path("getAtividade/<int:pk>", getAtividade, name="get-atividade"),
    
    # ROTAS PARA MEMBROS DE EXECUCAO
    path("membrosExecucaoTable",membrosExecucaoTable),
    path("membrosExecucaoDpEventoTable",membrosExecucaoDpEventoTable),
    path("membroExecucaoForm",membroExecucaoForm),
    path("membroExecucaoModal",membroExecucaoModal),
    path("saveMembroExecucao",saveMembroExecucao),
    path("membrosExecucaoSelect",membrosExecucaoSelect),
    path("getMembrosExecucao",getMembrosExecucao, name="membros-execucao-all"),
    path("get-membro-execucao/<int:pk>",getMembroExecucao, name="get-membro-execucao"),
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
    path("visualizarDpEvento/<codigo>", visualizarDpEvento, name="visualizar-dp-evento"),
    path("relatorioPorEvento/<evento_id>", relatorioPorEvento),
    path("relatorioDpEvento", relatorioDpEvento),
    path("relatorioSintetico", relatorioSintetico),
   
    # ROTAS PARA TICKETS
    path("ticketModal",ticketModal),
    path("ticketModalEdit/<ticket_id>",ticketModalEdit),
    path("saveTicket",saveTicket),
    path("editarTicket/<ticket_id>",editarTicket),
    path("updateTicket/<ticket_id>",updateTicket),
    path("ticket_form",ticket_form),
    path("ticket_form_collapsable",ticket_form_collapsable),
    path("eliminarTicket/<ticket_id>",eliminarTicket),
    
    # ROTAS PARA SERVICOS
    path("ServicoModalCadastrar",ServicoModalCadastrar),
    path("editarServico/<servico_id>",editarServico),
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
    path("confirmDeleteModal",confirmDeleteModal, name="confirm-delete-modal"),
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
    path("deleteGaleria/<galeria_id>", deleteGaleria),
    
    # ROTAS PARA MEMBRO EXECUCAO ROLES
    path("getMembroExecucaoRoles", getMembroExecucaoRoles, name="membro-execucao-roles-all"),
    path("membro-execucao-role-form", getMembroExecucaoRoleForm, name="membro-execucao-role-form"),
    path("membro-execucao-role-create", membroExecucaoRoleCreate, name="membro-execucao-role-create"),

    #ROTAS PARA SEÇÂO DE ATIVIDADES
    path("atividadeSectionModal", atividadeSectionModal),
    path("atividadeSectionTable", atividadeSectionTable),
    path("saveAtividadeSection", saveAtividadeSection),
    path("deleteAtividadeSection/<int:atividade_section_id>", deleteAtividadeSection),
    path("updateAtividadeSection/<int:atividade_section_id>", updateAtividadeSection),
    path("atividadeSectionComponent//<int:atividade_section_id>", atividadeSectionComponent),
    
    #ROTAS PARA RECURSOS
    path("recurso-form", recursoForm, name="recurso-form"),
    path("recurso-save", recursoSave, name="recurso-save"),
    path("recurso-edit/<int:recurso_id>", recursoEdit, name="recurso-edit"),
    path("recurso-tabela", recursoTabela, name="recurso-tabela"),
    path("recurso-delete/<int:recurso_id>", recursoDelete, name="recurso-delete"),      
    
    # ROTAS PARA IMAGENS
    path("saveImagem", saveImagem),
    path("deleteImagem/<imagem_id>", deleteImagem),
    
    # ROTAS PARA ANEXOS
    path("saveAnexo", saveAnexo),
    path("deleteAnexo/<anexo_id>", deleteAnexo),

    # ROTAS DE API
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    path("send-email", EmailApiView.as_view()),

    path("pessoas", PessoaApiView.as_view()),
    path("pessoas/<int:pessoa_id>", PessoaDetailApiView.as_view()),

    path("galerias", GaleriaApiView.as_view()),
    path("galerias/<int:galeria_id>", GaleriaDetailApiView.as_view()),
    
    path("imagens", ImagemApiView.as_view()),
    path("imagens/<int:imagem_id>", ImagemDetailApiView.as_view()),
    
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
   
    path("membroExecucao", MembroExecucaoApiView.as_view(), name="membroExecucao"),
    path('membroExecucao/<int:membro_execucao_id>', MembroExecucaoDetailApiView.as_view(), name="membroExecucaoDetail"),
    
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
    
    path("atividade-section", AtividadeSectionApiView.as_view()),
    path('atividade-section/<int:atividade_section_id>', AtividadeSectionDetailApiView.as_view()),

    path("anexos", AnexoApiView.as_view()),
    path('anexos/<int:anexo_id>', AnexoDetailApiView.as_view()),
    
    path("comentarios", ComentarioApiView.as_view()),
    path('comentarios/<int:comentario_id>', ComentarioDetailApiView.as_view()),
    
    path('membro-execucao-roles', MembroExecucaoRoleApiView.as_view(), name="membro-execucao-roles"),
    path('membro-execucao-roles/<int:membro_execucao_role_id>', MembroExecucaoRoleDetailApiView.as_view(), name="membro-execucao-role-detail"),

    path('recursos', RecursoApiView.as_view()),
    path('recursos/<int:recurso_id>', RecursoDetailApiView.as_view()),
    # ROTAS DE AUTENTICAÇÂO
    path("auth-user/", include('django.contrib.auth.urls')),
    path("auth-user/", include('authentication.urls')),

    path('', include(router.urls)),
]
