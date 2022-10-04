# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.endereco import Endereco

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = [
            "id",
            "endereco_completo"
        ]
