# todo/todo_api/views.py
from rest_framework.response import Response
from rest_framework import status as st, viewsets
from ..models.cidade import Cidade
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from ..models.pessoa import Pessoas
from ..models.ticket import Ticket
from ..models.atividade import Atividade
from ..models.membroExecucao import MembroExecucao
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import Count

def membro_execucao_por_pessoa(dpevento):
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
            
            print(pessoaId)
            membroExecucaoCreated = MembroExecucao.objects.create(**{
                'pessoa': Pessoas.objects.get(id=pessoaId),
                'evento': dpevento,
                'observacao': "",
            })

            for membroExecucao in membrosExecucao:
                ticket = membroExecucao.ticket_set.first()

                ticketCreated = Ticket.objects.create(**{
                    'tipo': membroExecucao.tipo,
                    'status': ticket.status,
                    'id_protocolo': ticket.id_protocolo,
                    'membro_execucao': membroExecucaoCreated,
                    'meta': ticket.meta,
                    'data_inicio': membroExecucao.data_inicio,
                    'data_fim': membroExecucao.data_fim,
                    'bairro': membroExecucao.bairro,
                    'logradouro': membroExecucao.logradouro,
                    'cep': membroExecucao.cep,
                    'complemento': membroExecucao.complemento,
                    'cidade': membroExecucao.cidade,
                })
                print(membroExecucao.id, membroExecucao.pessoa.id, ticket.id_protocolo)
                ticket.delete()
                membroExecucao.delete()

def create_dp_evento(acao):
    cidade, _ = Cidade.objects.get_or_create(nome=acao.cidade)
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
        print("migratreAcoes")
        for acao in Acao.objects.all():
            create_dp_evento(acao)
        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="migrate-membro-execucao")
    def migratreMembroExecucao(self, *args, **kwargs):
        print("migratreMembroExecucao")
        for evento in DpEvento.objects.all():
            membro_execucao_por_pessoa(evento)
        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
