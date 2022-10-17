# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.cidade import Cidade

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = [
            "id",
            "nome"
        ]
