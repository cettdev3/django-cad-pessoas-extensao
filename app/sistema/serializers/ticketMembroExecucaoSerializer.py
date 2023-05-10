# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.ticket import Ticket

class TicketMembroExecucaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "tipo",
            "status",
            "id_protocolo",
            "membro_execucao",
            "model",
            "observacao",
            "icon",
            "tipo_formatado",
            "status_class",
            "status_formatado",
            "status_calculado"
        ]
        depth = 1
