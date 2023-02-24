# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.servico import Servico

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = [
            "id",
            "nome",
            "quantidadeAtendimentos",
            "quantidadeVendas",
            "atividade",
        ]
