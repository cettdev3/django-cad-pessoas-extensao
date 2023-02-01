# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.alocacao import Alocacao
from ..models.atividade import Atividade

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = [
            "id",
            "descricao",
            "linkDocumentos",
            "status",
            "acao",
            "evento",
            "tipoAtividade",
            "responsavel",
            "departamento",
            "cidade",
            "logradouro",
            "bairro",
            "cep",
            "complemento"
        ]
        depth = 2
