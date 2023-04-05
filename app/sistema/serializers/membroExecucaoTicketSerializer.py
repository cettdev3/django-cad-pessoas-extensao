# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.membroExecucao import MembroExecucao
from .dpEventoTicketSerializer import DpEventoTicketSerializer

class MembroExecucaoTicketSerializer(serializers.ModelSerializer):
    evento = DpEventoTicketSerializer(many=False, read_only=True)

    class Meta:
        model = MembroExecucao
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "tipo",
            "evento",
            "complemento",
            "cidade",
            "avaliador",
            "pessoa",
        ]
        depth = 2
