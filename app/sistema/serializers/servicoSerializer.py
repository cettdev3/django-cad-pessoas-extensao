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
            "cidade",
            "logradouro",
            "bairro",
            "cep",
            "complemento",
            "status",
            "descricao",
            "status_formatado"
    ]
    depth = 2
