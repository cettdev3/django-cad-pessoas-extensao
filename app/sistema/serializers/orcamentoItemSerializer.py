# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.orcamentoItem import OrcamentoItem
class OrcamentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoItem
        fields = [
            "id",
            "descricao",
            "tipo",
            "quantidade",
            "unidade",
            "valor",
            "valor_total",
            "em_estoque",
        ]
