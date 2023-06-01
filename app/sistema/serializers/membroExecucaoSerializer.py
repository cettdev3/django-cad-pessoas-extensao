# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.membroExecucao import MembroExecucao
from ..models.ticket import Ticket
from .itinerarioSerializer import ItinerarioSerializer
from .ticketSerializers.ticketSerializer import TicketSerializer

class MembroExecucaoSerializer(serializers.ModelSerializer):
    itinerario = ItinerarioSerializer(many=False, read_only=True)
    ticket_set = TicketSerializer(many=True, read_only=True)

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
            "avaliador",
            "pessoa",
            "ticket_set",
            "itinerario",
            "ticket_status"
        ]
        depth = 4
