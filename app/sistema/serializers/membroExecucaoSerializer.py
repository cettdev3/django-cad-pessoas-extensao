# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.membroExecucao import MembroExecucao

class MembroExecucaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembroExecucao
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "bairro",
            "tipo",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
            "pessoa",
        ]
        depth = 1
