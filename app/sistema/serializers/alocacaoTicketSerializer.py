# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.alocacao import Alocacao
from ..serializers.dataRemovidaSerializer import DataRemovidaSerializer

class AlocacaoTicketSerializer(serializers.ModelSerializer):
    endereco_completo = serializers.CharField(read_only=True)
    data_inicio_formatada = serializers.CharField(read_only=True)
    data_fim_formatada = serializers.CharField(read_only=True)

    class Meta:
        model = Alocacao
        fields = [
            "id",
            "acaoEnsino",
            "professor",
            "data_inicio",
            "data_fim",
            "data_inicio_formatada",
            "data_fim_formatada",
            "endereco_completo",
            "status",
            "cidade",
        ]
        depth = 2
