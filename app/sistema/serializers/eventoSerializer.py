# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.evento import Evento

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "observacao",
            "cidade",
            "enderecos",
        ]
