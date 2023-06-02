# todo/todo_api/views.py
from rest_framework.response import Response
from rest_framework import status as st, viewsets
from ..models.cidade import Cidade
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from ..models.pessoa import Pessoas
from ..models.atividadeCategoria import AtividadeCategoria
from ..models.ticket import Ticket
from ..models.atividadeSection import AtividadeSection
from ..models.galeria import Galeria
from ..models.dpEventoEscola import DpEventoEscola
from ..models.atividade import Atividade
from ..models.membroExecucao import MembroExecucao
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import Count

def membro_execucao_por_pessoa(dpevento):
    with transaction.atomic():
        membros_por_pessoa = MembroExecucao.objects.filter(
            evento=dpevento
        ).select_related(
            'pessoa'
        ).order_by(
            'pessoa__id'
        )

        result = []
        current_pessoa_id = None
        current_membros = []

        for membro in membros_por_pessoa:
            if membro.pessoa_id != current_pessoa_id:
                if current_pessoa_id is not None:
                    result.append({current_pessoa_id: current_membros})
                current_pessoa_id = membro.pessoa_id
                current_membros = [membro]
            else:
                current_membros.append(membro)

        if current_pessoa_id is not None:
            result.append({current_pessoa_id: current_membros})
        for item in result:
            for pessoaId, membrosExecucao in item.items():
                
                membroExecucaoCreated = MembroExecucao.objects.create(**{
                    'pessoa': Pessoas.objects.get(id=pessoaId),
                    'evento': dpevento,
                    'observacao': "",
                })
                
                for membroExecucao in membrosExecucao:
                    ticketCreated = None
                    membroExecucaoId = membroExecucao.id
                    for ticket in membroExecucao.ticket_set.all():
                        ticketCreated = Ticket.objects.create(**{
                            'tipo': membroExecucao.tipo,
                            'status': ticket.status if ticket else "CREATED",
                            'id_protocolo': ticket.id_protocolo if ticket else None,
                            'membro_execucao': membroExecucaoCreated,
                            'meta': ticket.meta if ticket else None,
                            'data_inicio': membroExecucao.data_inicio,
                            'data_fim': membroExecucao.data_fim,
                            'bairro': membroExecucao.bairro,
                            'logradouro': membroExecucao.logradouro,
                            'cep': membroExecucao.cep,
                            'complemento': membroExecucao.complemento,
                            'cidade': membroExecucao.cidade,
                        })
                        ticket.delete()
                    membroExecucao.delete()
                    try:
                        membroExecucao = MembroExecucao.objects.get(id=membroExecucaoId)    
                    except MembroExecucao.DoesNotExist:
                        membroExecucao = None
                    finally:
                        print("membro execucao id depois delete: ", membroExecucaoId, membroExecucao)
                    
def create_dp_evento(acao):
    with transaction.atomic():
        cidade = Cidade.objects.get(id=acao.cidade.id)
        dp_evento = DpEvento.objects.create(
            tipo=acao.tipo,
            process_instance=acao.process_instance,
            status=acao.status,
            descricao=acao.descricao,
            data_inicio=acao.data_inicio,
            data_fim=acao.data_fim,
            bairro=acao.bairro,
            logradouro=acao.logradouro,
            cep=acao.cep,
            complemento=acao.complemento,
            cidade=cidade,
            escola=acao.escola,
        )
        for membro_execucao in acao.membroexecucao_set.all():
            membroExecucao = MembroExecucao.objects.get(id=membro_execucao.id)
            membroExecucao.evento = dp_evento
            membroExecucao.save()
        for atividade in acao.atividade_set.all():
            atividade = Atividade.objects.get(id=atividade.id)
            atividade.evento = dp_evento
            atividade.save()

class MigrationsViewSets(viewsets.ModelViewSet):

    @action(methods=["POST"], detail=False, url_path="migrate-acoes")
    def migratreAcoes(self, *args, **kwargs):
        for acao in Acao.objects.all():
            create_dp_evento(acao)
        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    
    @action(methods=["POST"], detail=False, url_path="migrate-tickets")
    def migratreTickets(self, *args, **kwargs):
        for ticket in Ticket.objects.all():
            if ticket.status == "EM_DIAS":
                ticket.status = ticket.STATUS_CRIACAO_PENDENTE
            if ticket.status == "CREATED":
                ticket.status = ticket.STATUS_CRIADO
            ticket.save()

        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="migrate-membro-execucao")
    def migratreMembroExecucao(self, *args, **kwargs):
        for evento in DpEvento.objects.all():
            membro_execucao_por_pessoa(evento)
        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="seed-atividades-galeria")
    def seedAtividadesGaleria(self, *args, **kwargs):
        for atividade in Atividade.objects.all():
            if atividade.galeria:
                continue
            nome = "galeria: "+atividade.tipoAtividade.nome if atividade.tipoAtividade else "galeria"
            atividade.galeria = Galeria.objects.create(
                nome=nome,
                evento=atividade.evento,
            )
            atividade.save()
        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="transferir-evento-escola")
    # devido a mudança no modelo de dados, foi necessário transferir a escola do evento para a pivot eventos_escolas
    def transferirEventoEscola(self, *args, **kwargs):
        for evento in DpEvento.objects.all():
            if evento.escola:
                evento_escola = DpEventoEscola.objects.create(
                    escola=evento.escola,
                    dp_evento=evento,
                )
        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="update-beneficiario-tickets")
    # devido a mudança no modelo de dados, foi necessário adicionar o beneficiario nos tickets
    def criarBeneficiariosTickets(self, *args, **kwargs):
        with transaction.atomic():
            for ticket in Ticket.objects.all():
                if ticket.membro_execucao:
                    ticket.beneficiario = ticket.membro_execucao.pessoa
                    ticket.model = 'beneficiario'
                    escolas = ticket.membro_execucao.evento.escolas.all()
                    if len(escolas) > 0:
                        ticket.escola = escolas[0]

                if ticket.pessoa:
                    ticket.beneficiario = ticket.pessoa
                    ticket.model = 'beneficiario'

                if ticket.alocacao:
                    ticket.escola = ticket.alocacao.acaoEnsino.escola
                    ticket.beneficiario = ticket.alocacao.professor
                    ticket.model = 'beneficiario'

                ticket.save()
        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="create-secao-atividades")
    # devido a mudança no modelo de dados, foi necessário adicionar o beneficiario nos tickets
    def criarSecaoAtividades(self, *args, **kwargs):
        with transaction.atomic():
            for evento in DpEvento.objects.all():
                atividadeSection = AtividadeSection()
                atividadeSection.evento = evento
                atividadeSection.nome = 'Seção de atividades'
                atividadeSection.order = 1
                atividadeSection.save()

                for atividade in Atividade.objects.filter(evento=evento):
                    atividade.atividadeSection = atividadeSection
                    if atividade.status == 'realizada':
                        atividade.status = 'concluido'
                    atividade.save()

        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")

    @action(methods=["POST"], detail=False, url_path="update-atividades-extensao")
    def updateAtividadesExtensao(self, *args, **kwargs):
        with transaction.atomic():
            for atividade in Atividade.objects.all():
                if atividade.atividade_meta:
                    atividade.categoria = atividade.CATEGORIA_META_EXTENSAO
                    atividade.nome = atividade.descricao
                    atividade.save()

        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")

    @action(methods=["POST"], detail=False, url_path="create-atividade-categorias")
    def updateAtividadesExtensao(self, *args, **kwargs):
        CATEGORIA_TAREFA = 'tarefa'
        CATEGORIA_PROGRAMACAO = 'programacao'
        CATEGORIA_META_EXTENSAO = 'meta_extensao'
        CATEGORIA_REUNIAO = 'reuniao'
        CATEGORIA_MARCO = 'marco'
        CATEGORIA_SUBTAREFAS = 'subtarefa'
        CATEGORIA_ATIVIDADE = 'atividade'
        categories = [
            ('Tarefa', 'badge-categoria-tarefa', CATEGORIA_TAREFA),
            ('Programação', 'badge-categoria-programacao', CATEGORIA_PROGRAMACAO),
            ('Meta de Extensão', 'badge-categoria-meta-extensao', CATEGORIA_META_EXTENSAO),
            ('Reunião', 'badge-categoria-reuniao', CATEGORIA_REUNIAO),
            ('Marco', 'badge-categoria-marco', CATEGORIA_MARCO),
            ('Subtarefa', 'badge-categoria-subtarefas', CATEGORIA_SUBTAREFAS),
            ('Atividade', 'badge-categoria-atividade', CATEGORIA_ATIVIDADE),
        ]

        for name, badge, slug in categories:
            AtividadeCategoria.objects.get_or_create(name=name, badge=badge, slug=slug)

        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")

    @action(methods=["POST"], detail=False, url_path="set-atividade-categorias")
    def setAtividadesExtensao(self, *args, **kwargs):
        atividades = Atividade.objects.all()
        atividadeCategorias = AtividadeCategoria.objects.all()

        for atividade in atividades:
            for categoria in atividadeCategorias:
                if atividade.categoria == categoria.slug:
                    atividade.atividadeCategorias.add(categoria)
                    atividade.save()

        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")
