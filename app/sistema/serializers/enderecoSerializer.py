# todo/todo_api/serializers.py
from rest_framework import serializers

from ..serializers.cidadeSerializer import CidadeSerializer
from ..models.endereco import Endereco

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = [
            "id",
            "endereco_completo",
            "cidade"
        ]
        depth = 1
