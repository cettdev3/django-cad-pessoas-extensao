# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.servicoContratado import ServicoContratado
from .dpEventoSerializer import DpEventoSerializer
from .membroExecucaoSerializer import MembroExecucaoSerializer
class ServicoContratadoSerializer(serializers.ModelSerializer):
    evento = DpEventoSerializer(many=False, read_only=True)
    responsavel = MembroExecucaoSerializer(many=False, read_only=True)
    class Meta:
        model = ServicoContratado
        fields = [
            "id",
            "descricao",
            "valor",
            "data_limite",
            "evento",
            "responsavel"
        ]

        depth = 2
