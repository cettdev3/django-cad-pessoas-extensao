# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.avaliacao import Avaliacao

class AvaliacaoSerializer(serializers.ModelSerializer):
    endereco_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Avaliacao
        fields = [
            "id",
            "acao",
            "evento",
            "avaliador",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "endereco_completo"
        ]
        depth = 3
