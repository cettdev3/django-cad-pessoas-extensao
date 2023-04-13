# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.servicoContratado import ServicoContratado
from .dpEventoSerializer import DpEventoSerializer
class ServicoContratadoSerializer(serializers.ModelSerializer):
    evento = DpEventoSerializer(many=False, read_only=True)
    class Meta:
        model = ServicoContratado
        fields = [
            "id",
            "descricao",
            "valor",
            "data_limite",
            "evento",
        ]

        depth = 2
