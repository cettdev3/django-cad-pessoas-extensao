# todo/todo_api/views.py
from rest_framework.response import Response
from rest_framework import status as st, viewsets
from ..models.cidade import Cidade
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from ..models.pessoa import Pessoas
from ..models.ticket import Ticket
from ..models.galeria import Galeria
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
                
                print("pessoa id: ",pessoaId)
                membroExecucaoCreated = MembroExecucao.objects.create(**{
                    'pessoa': Pessoas.objects.get(id=pessoaId),
                    'evento': dpevento,
                    'observacao': "",
                })
                
                for membroExecucao in membrosExecucao:
                    print("membro execucao id: ", membroExecucao.id)
                    ticketCreated = None
                    membroExecucaoId = membroExecucao.id
                    for ticket in membroExecucao.ticket_set.all():
                        print("ticket id: ", ticket.id)
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
                    print(membroExecucaoCreated.id)
                    print("membro execucao id antes delete: ", membroExecucaoId, membroExecucao)
                    membroExecucao.delete()
                    try:
                        membroExecucao = MembroExecucao.objects.get(id=membroExecucaoId)    
                        print("membro execucao id depois delete: ", membroExecucaoId, membroExecucao)
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
        print("migratreAcoes")
        for acao in Acao.objects.all():
            create_dp_evento(acao)
        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    
    @action(methods=["POST"], detail=False, url_path="migrate-tickets")
    def migratreTickets(self, *args, **kwargs):
        print("migratreTickets")
        for ticket in Ticket.objects.all():
            print("ticket status: ", ticket.status)
            if ticket.status == "EM_DIAS":
                print("ticket status if 1: ", ticket.status)
                ticket.status = ticket.STATUS_CRIACAO_PENDENTE
            if ticket.status == "CREATED":
                print("ticket status if 2: ", ticket.status)
                ticket.status = ticket.STATUS_CRIADO
            ticket.save()

        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="migrate-membro-execucao")
    def migratreMembroExecucao(self, *args, **kwargs):
        print("migratreMembroExecucao")
        for evento in DpEvento.objects.all():
            membro_execucao_por_pessoa(evento)
        return Response(data={}, status=st.HTTP_201_CREATED, content_type="application/json")
    
    @action(methods=["POST"], detail=False, url_path="seed-atividades-galeria")
    def seedAtividadesGaleria(self, *args, **kwargs):
        for atividade in Atividade.objects.all():
            if atividade.galeria:
                continue
            
            atividade.galeria = Galeria.objects.create(
                nome="galeria: "+atividade.tipoAtividade.nome,
                evento=atividade.evento,
            )
            atividade.save()
        return Response(data={}, status=st.HTTP_200_OK, content_type="application/json")
