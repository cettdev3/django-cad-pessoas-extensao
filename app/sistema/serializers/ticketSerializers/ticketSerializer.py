# todo/todo_api/serializers.py
from rest_framework import serializers
from ...models.ticket import Ticket
from .membroExecucaoTicketSerializer import MembroExecucaoTicketSerializer
from .alocacaoTicketSerializer import AlocacaoTicketSerializer
from .escolaTicketSerializer import EscolaTicketSerializer
from .pessoaTicketSerializer import PessoaTicketSerializer
from .pessoaTicketSerializer import PessoaTicketSerializer
from .atividadeTicketSerializer import AtividadeTicketSerializer
class TicketSerializer(serializers.ModelSerializer):
    meta = serializers.JSONField(allow_null=True)
    membro_execucao = MembroExecucaoTicketSerializer(many=False, read_only=True)
    alocacao = AlocacaoTicketSerializer(many=False, read_only=True)
    pessoa = PessoaTicketSerializer(many=False, read_only=True)
    escola = EscolaTicketSerializer(many=False, read_only=True)
    status_formatado = serializers.CharField(read_only=True)
    status_calculado = serializers.CharField(read_only=True)
    atividade = AtividadeTicketSerializer(many=False, read_only=True)
    class Meta:
        model = Ticket
        fields = [
            "id",
            "tipo",
            "status",
            "id_protocolo",
            "membro_execucao",
            "alocacao",
            "pessoa",
            "escola",
            "meta",
            "model",
            "data_inicio",
            "data_fim",
            "data_inicio_formatada",
            "data_fim_formatada",
            "nao_se_aplica_data_inicio",
            "nao_se_aplica_data_fim",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
            "observacao",
            "atividade",
            "endereco_completo",
            "icon",
            "tipo_formatado",
            "status_class",
            "status_formatado",
            "status_calculado"
        ]
        depth = 2
