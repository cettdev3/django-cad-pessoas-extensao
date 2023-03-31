# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.ticket import Ticket

class TicketSerializer(serializers.ModelSerializer):
    meta = serializers.JSONField(allow_null=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "tipo",
            "status",
            "id_protocolo",
            "membro_execucao", 
            "meta",
            "icon",
            "status_class",
            "status_formatado",
            "tipo_formatado"
        ]
        depth = 2
