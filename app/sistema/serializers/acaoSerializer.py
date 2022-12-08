# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.acao import Acao
from ..models.cidade import Cidade

class AcaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acao
        fields = [
            "id",
            "tipo",
            "process_instance",
            "variaveis",
            "status",
            "descricao",
            "data_inicio",
            "data_fim",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
        ]
        depth = 1
