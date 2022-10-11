# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.alocacao import Alocacao

class AlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alocacao
        fields = [
            "id",
            "evento",
            "professor",
            "data_inicio",
            "data_fim",
            "status",
            "observacao",
        ]
        depth = 2
