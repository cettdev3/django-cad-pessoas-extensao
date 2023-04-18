from django.db import transaction
from ..models import Ticket, MembroExecucao, Alocacao, Cidade, ServicoContratado

def create_ticket(
    tipo,
    status,
    id_protocolo,
    membro_execucao_id=None,
    alocacao_id=None,
    servico_contratado_id=None,
    meta=None,
    model=None,
    data_inicio=None,
    data_fim=None,
    nao_se_aplica_data_inicio=False,
    nao_se_aplica_data_fim=False,
    bairro=None,
    logradouro=None,
    cep=None,
    complemento=None,
    cidade_id=None,
    observacao=None,
):
    with transaction.atomic():
        membro_execucao = (
            MembroExecucao.objects.get(pk=membro_execucao_id)
            if membro_execucao_id
            else None
        )
        alocacao = (
            Alocacao.objects.get(pk=alocacao_id)
            if alocacao_id
            else None
        )
        cidade = (
            Cidade.objects.get(pk=cidade_id)
            if cidade_id
            else None
        )

        servico_contratado = (
            ServicoContratado.objects.get(pk=servico_contratado_id)
            if servico_contratado_id
            else None
        )

        ticket = Ticket(
            tipo=tipo,
            status=status,
            id_protocolo=id_protocolo,
            membro_execucao=membro_execucao,
            alocacao=alocacao,
            meta=meta,
            model=model,
            data_inicio=data_inicio,
            data_fim=data_fim,
            nao_se_aplica_data_inicio=nao_se_aplica_data_inicio,
            nao_se_aplica_data_fim=nao_se_aplica_data_fim,
            bairro=bairro,
            logradouro=logradouro,
            cep=cep,
            complemento=complemento,
            cidade=cidade,
            observacao=observacao,
            servico_contratado=servico_contratado,
        )
        ticket.save()
        return ticket