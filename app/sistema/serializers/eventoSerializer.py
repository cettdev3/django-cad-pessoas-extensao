# todo/todo_api/serializers.py
from rest_framework import serializers

from .enderecoSerializer import EnderecoSerializer

from ..models.endereco import Endereco
from ..models.evento import Evento

class EventoSerializer(serializers.ModelSerializer):
    data_inicio = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    data_fim = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')

    class Meta:
        model = Evento
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "observacao",
            "status",
            "endereco",
            "status_class",
            "logradouro",
            "complemento",
            "bairro",
            "cidade",
            "cep",
        ]
        depth = 2
        
