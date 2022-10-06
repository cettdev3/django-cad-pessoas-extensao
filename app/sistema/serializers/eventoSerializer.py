# todo/todo_api/serializers.py
from rest_framework import serializers

from .enderecoSerializer import EnderecoSerializer

from ..models.endereco import Endereco
from ..models.evento import Evento

class EventoSerializer(serializers.ModelSerializer):
    data_inicio = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    data_fim = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Evento
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "observacao",
            "endereco",
        ]
        depth = 2
        
