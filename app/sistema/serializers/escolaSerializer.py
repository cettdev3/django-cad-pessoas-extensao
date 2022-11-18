# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.escola import Escola

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = [
            "id",
            "nome",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade"
        ]
        depth = 2
