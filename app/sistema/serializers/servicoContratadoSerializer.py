# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.servicoContratado import ServicoContratado

class ServicoContratadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoContratado
        fields = [
            "id",
            "descricao",
            "valor",
            "data_limite"
        ]
