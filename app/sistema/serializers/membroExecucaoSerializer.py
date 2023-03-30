# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.membroExecucao import MembroExecucao
from .itinerarioSerializer import ItinerarioSerializer

class MembroExecucaoSerializer(serializers.ModelSerializer):
    itinerario = ItinerarioSerializer(many=False, read_only=True)
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
            "ticket",
            "itinerario"
        ]
        depth = 4
