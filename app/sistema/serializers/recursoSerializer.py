# todo/todo_api/serializers.py
from rest_framework import serializers
from sistema.models import (
    Recursos
)

class RecursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recursos
        fields = [
            "id",
            "proposta_projeto",
            "nome",
            "descricao",
            "quantidade",
            "unidade",
            "valor",
            "valor_total",
            "em_estoque",
        ]
