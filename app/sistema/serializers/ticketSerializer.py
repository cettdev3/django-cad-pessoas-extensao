# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.ticket import Ticket

class TicketSerializer(serializers.ModelSerializer):
    meta = serializers.JSONField(allow_null=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "tipo",
            "status",
            "id_protocolo",
            "membro_execucao",
            "meta",
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
            "endereco_completo",
            "icon",
            "tipo_formatado",
            "status_class",
            "status_formatado",
        ]
        depth = 2
