# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.orcamento import Orcamento
from ..serializers.orcamentoItemSerializer import OrcamentoItemSerializer

class OrcamentoSerializer(serializers.ModelSerializer):
    items = OrcamentoItemSerializer(many=True, read_only=True)
    class Meta:
        model = Orcamento
        fields = [
            "id",
            "items"
        ]
