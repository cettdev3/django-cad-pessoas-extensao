# todo/todo_api/serializers.py
from rest_framework import serializers
from ...models.atividade import Atividade
from .dpEventoTicketSerializer import DpEventoTicketSerializer

class AtividadeTicketSerializer(serializers.ModelSerializer):
    evento = DpEventoTicketSerializer(many=False, read_only=True)
    class Meta:
        model = Atividade
        fields = [
            "id",
            "descricao",
            "evento"
        ]
        depth = 2
