# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.alocacao import Alocacao
from ..serializers.dataRemovidaSerializer import DataRemovidaSerializer
from ..serializers.ticketSerializer import TicketSerializer

class AlocacaoSerializer(serializers.ModelSerializer):
    dataremovida_set = DataRemovidaSerializer(many=True, read_only=True)
    endereco_completo = serializers.CharField(read_only=True)
    data_inicio_formatada = serializers.CharField(read_only=True)
    data_fim_formatada = serializers.CharField(read_only=True)
    ticket_set = TicketSerializer(many=True, read_only=True)
    class Meta:
        model = Alocacao
        fields = [
            "id",
            "acaoEnsino",
            "professor",
            "curso",
            "data_inicio",
            "data_fim",
            "data_inicio_formatada",
            "data_fim_formatada",
            "endereco_completo",
            "status",
            "observacao",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
            "turnos",
            "ticket_set",
            "aulas_sabado",
            "dataremovida_set",
        ]
        depth = 2
